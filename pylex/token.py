"""Token (lexeme) class."""


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

    def is_end(self):
        """Return whether this token is either an EOF or EOL token."""

        return self.category == Token.EOF or self.category == Token.EOL

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
