"""Scanner generator implementation."""

from pylex import NUM_SYMBOLS


class _ScannerGenerator:
    """A scanner generator: converts a DFA to code which recognizes the same
    regular language.

    The generated scanner is greedy - it lexes the longest possible token when
    it is called. The specifics for the interface depend on the language in
    which the scanner was generated.

    """

    def __init__(self, dfa):
        """Create a scanner generator that recognizes the same language as the
        given DFA.

        Arguments:
        dfa -- The DFA to generate a scanner for.

        """

        self._table = []
        self._accepting = []
        self._states = {}
        self._create_table(dfa.initial)
        del self._states

    def _create_table(self, state):
        if not state in self._states:
            assert len(self._states) == len(self._table) == len(self._accepting)
            self._states[state] = len(self._states)
            self._accepting.append(state.accepting if state.accepting else 0)
            self._table.append([-1] * NUM_SYMBOLS)
        index = self._states[state]

        for (symbol, target) in state.transitions.items():
            if target not in self._states:
                self._create_table(target)
            target_index = self._states[target]

            self._table[index][ord(symbol)] = target_index

    def c_source(self):
        """Return the C source code for the scanner as a string.

        The scanner is returned as a function specified as follows:

        /**
         * Lex a token from the given stream.
         * @param category_out Return parameter for the syntactic category of
         * the token.
         * @return The malloc-allocated lexeme; can be freed with free. NULL if
         * the scanner failed to find a token.
         */
        char *pylex(FILE *file, int *category_out);
        """

        raise NotImplementedError


class TableDrivenScannerGenerator(_ScannerGenerator):
    """Scanner generator for a table-driven scanner."""

    def __init__(self, dfa):
        super().__init__(dfa)

    def c_source(self):
        def initializer_list(l):
            return '{{{}}}'.format(', '.join(str(x) for x in l))

        def nested_initializer_list(ll):
            initializer_lists = ('    ' + initializer_list(l) + ',' for l in ll)
            return '{{\n{}\n}}'.format('\n'.join(initializer_lists))

        includes = \
"""\
#include <stdio.h>
#include <stdlib.h>
"""

        tables = \
"""
static int accepting[] = {};
static int transitions[][{}] = {};
""".format(initializer_list(self._accepting), NUM_SYMBOLS,
           nested_initializer_list(self._table))

        body = \
"""
static int *backtrack_stack = NULL;
static size_t stack_size = 0;
static size_t stack_capacity = 0;

#define PUSH_STACK(state) \\
    do { \\
        if (stack_size == stack_capacity) { \\
            if (stack_capacity == 0) \\
                stack_capacity = 64; \\
            else \\
                stack_capacity *= 2; \\
            backtrack_stack = realloc(backtrack_stack, stack_capacity * sizeof(int)); \\
            if (!backtrack_stack) { \\
                fprintf(stderr, "pylex: memory exhausted\\n"); \\
                exit(EXIT_FAILURE); \\
            } \\
        } \\
        backtrack_stack[stack_size++] = state; \\
    } while (0);

char *pylex(FILE *file, int *category_out)
{
    char *lexeme = NULL;
    size_t lexeme_size = 0;
    size_t lexeme_capacity = 0;

#define APPEND_TO_LEXEME(c) \\
    do { \\
        if (lexeme_size == lexeme_capacity) { \\
            if (lexeme_capacity == 0) \\
                lexeme_capacity = 64; \\
            else \\
                lexeme_capacity *= 2; \\
            lexeme = realloc(lexeme, lexeme_capacity); \\
            if (!lexeme) { \\
                fprintf(stderr, "pylex: memory exhausted\\n"); \\
                exit(EXIT_FAILURE); \\
            } \\
        } \\
        lexeme[lexeme_size++] = c; \\
    } while (0);

    stack_size = 0;

    int curstate = 0;

    do {
        char c = getc(file);
        if (c == EOF)
            break;

        APPEND_TO_LEXEME(c);

        if (accepting[curstate])
            stack_size = 0;
        PUSH_STACK(curstate);

        curstate = transitions[curstate][(unsigned char) c];
    } while (curstate != -1);

    while (!accepting[curstate] && stack_size > 0) {
        curstate = backtrack_stack[--stack_size];

        if (ungetc(lexeme[--lexeme_size], file) == EOF) {
            fprintf(stderr, "pylex: backtracking error\\n");
            exit(EXIT_FAILURE);
        }
    }

    if (accepting[curstate]) {
        *category_out = accepting[curstate];
        APPEND_TO_LEXEME('\\0');
        return lexeme;
    } else {
        *category_out = -1;
        return NULL;
    }
}
"""

        return includes + tables + body
