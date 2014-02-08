"""Lexical analysis phase of the regular expression compiler."""


class Token:
    """A token (a.k.a. lexeme) in a regular expression.

    Attributes:
    category -- The syntactic category of this token. One of:
        EOF    -- End of file
        EOL    -- Newline '\\n'
        STAR   -- Asterisk '*'
        PIPE   -- Pipe '|'
        LPAREN -- Left parentheses '('
        RPAREN -- Right parentheses ')'
        SYMBOL -- A symbol in the language
    symbol -- If category is SYMBOL, the corresponding symbol (character) for
    this token.

    """

    EOF = 0
    EOL = 1
    STAR = 2
    PIPE = 3
    LPAREN = 4
    RPAREN = 5
    SYMBOL = 6

    _category_to_str = {
        EOF: "EOF",
        EOL: "EOL",
        STAR: "STAR",
        PIPE: "PIPE",
        LPAREN: "LPAREN",
        RPAREN: "RPAREN",
        SYMBOL: "SYMBOL",
    }

    def __init__(self, category, symbol=None):
        """Create a new token.

        Arguments:
        category -- The syntactic category of this token.
        symbol -- If category is SYMBOL, this must be a character. Ignored
        otherwise.

        """
        self.category = category
        if self.category == Token.SYMBOL:
            assert symbol and len(symbol) == 1
            self.symbol = symbol

    def __repr__(self):
        if self.category == Token.SYMBOL:
            return 'Token(SYMBOL, {})'.format(repr(self.symbol))
        else:
            return 'Token({})'.format(self._category_to_str[self.category])

    def __str__(self):
        if self.category == Token.SYMBOL:
            return 'SYMBOL({})'.format(repr(self.symbol))
        else:
            return self._category_to_str[self.category]


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
