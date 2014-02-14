"""Lexical analysis phase of the regular expression compiler."""

from pylex import SIGMA
from pylex.token import Token


class ScanningError(Exception):
    """Error encountered while scanning."""

    pass


class RegexScanner:
    """A regular expression scanner (a.k.a. lexer)."""

    _char_to_category = {
        '': Token.EOF,
        '\n': Token.EOL,
        '*': Token.STAR,
        '+': Token.PLUS,
        '|': Token.PIPE,
        '(': Token.LPAREN,
        ')': Token.RPAREN,
    }

    _escape_sequence = {
        '0': '\0',
        'a': '\a',
        'b': '\b',
        't': '\t',
        'n': '\n',
        'v': '\v',
        'f': '\f',
        'r': '\r',
    }

    def __init__(self, input, log_file=None):
        """Create a new scanner over a file or string.

        Arguments:
        input -- Either a file or a string over which to scan.
        log_file -- An optional file to which a log of lexed tokens is emitted.

        """

        self._input = input
        self._log_file = log_file

    def close(self):
        """Close the input file.

        The scanner may no longer be used. If the scanner contains a string, do
        nothing.

        """

        try:
            self._input.close()
        except AttributeError:
            pass
        self._input = None

    def _getc(self):
        """Read a single character from the input and advance the position of
        the input.

        Returns:
        The character read or an empty string on EOF.

        """

        try:
            c = self._input.read(1)
        except AttributeError:
            c, self._input = self._input[0:1], self._input[1:]
        return c

    def lex(self):
        """Lex a single token from the input.

        If the file is at EOF or the entire string has been consumed, returns
        an EOF token.

        """

        c = self._getc()

        if c == '\\':
            token = self._lex_escape_sequence()
        elif c == '[':
            token = self._lex_char_class()
        else:
            token = Token(self._char_to_category.get(c, Token.SYMBOL), c)

        if self._log_file:
            end = '\n' if token.is_end() else ' '
            print(token, file=self._log_file, end=end)

        return token
    
    def _lex_escape_sequence(self):
        """Lex an escape sequence assuming the backslash has already been
        consumed.

        """

        c = self._getc()
        if c == '':
            raise ScanningError('trailing backslash')
        elif c in self._escape_sequence:
            return Token(Token.SYMBOL, self._escape_sequence[c])
        else:
            return Token(Token.SYMBOL, c)

    def _lex_char_class(self):
        """Lex a character class assuming the opening bracket has already been
        consumed.

        """

        characters = set()
        inverted = False

        c = self._getc()
        if c == '^':
            inverted = True
            c = self._getc()

        if c == ']':
            # If there is a ']' at the beginning of the character class, it is
            # literal.
            characters.add(']')
            c = self._getc()

        range_start = ''
        prev_c = ''

        while c and c != ']':
            if c == '-':
                if prev_c:
                    range_start = prev_c
                else:
                    characters.add('-')
            else:
                if range_start:
                    assert prev_c == '-'
                    start_i = ord(range_start)
                    end_i = ord(c)
                    if end_i < start_i:
                        raise ScanningError('invalid range end')
                    range_start = ''
                    characters.update(chr(c) for c in range(start_i, end_i + 1))
                else:
                    characters.add(c)
            prev_c, c = c, self._getc()

        if not c:
            raise ScanningError('unmatched [ or [^')

        if prev_c == '-':
            # Trailing hyphen, literal.
            if range_start:
                characters.add(range_start)
            characters.add('-')

        if inverted:
            return Token(Token.CHARCLASS, set(SIGMA) - characters)
        else:
            return Token(Token.CHARCLASS, characters)
