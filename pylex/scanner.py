"""Lexical analysis phase of the regular expression compiler."""

from pylex.token import Token


class Scanner:
    """A scanner (a.k.a. lexer) over a file."""

    _char_to_category = {
        '': Token.EOF,
        '\n': Token.EOL,
        '*': Token.STAR,
        '|': Token.PIPE,
        '(': Token.LPAREN,
        ')': Token.RPAREN,
    }

    def __init__(self, file, log_file=None):
        """Create a new scanner over a file.

        Arguments:
        file -- The file over which to scan.
        log_file -- An optional file to which a log of lexed tokens is emitted.

        """

        self._file = file
        self._log_file = log_file

    def close(self):
        """Close the input file. The scanner may no longer be used."""
        self._file.close()

    def lex(self):
        """
        Lex a single token from the input file. If the file is at EOF, returns
        an EOF token.

        >>> scanner = Scanner(open('/dev/null', 'r'))
        >>> scanner.lex()
        Token(EOF)
        >>> scanner.close()
        >>> scanner = Scanner(open('/dev/zero', 'r'))
        >>> scanner.lex()
        Token(SYMBOL, '\\x00')
        >>> scanner.close()
        """

        c = self._file.read(1)
        token = Token(self._char_to_category.get(c, Token.SYMBOL), c)

        if self._log_file:
            end = '\n' if token.category in [Token.EOL, Token.EOF] else ' '
            print(token, file=self._log_file, end=end)

        return token
