"""Lexical analysis phase of the regular expression compiler."""

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
