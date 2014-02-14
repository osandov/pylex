"""Token (lexeme) class."""

from pylex import SIGMA


class Token:
    """A token (a.k.a. lexeme) in a regular expression.

    Attributes:
    category -- The syntactic category of this token. One of:
        EOF       -- End of file
        EOL       -- Newline '\\n'
        STAR      -- Asterisk '*'
        PLUS      -- Plus '+'
        PIPE      -- Pipe '|'
        LPAREN    -- Left parentheses '('
        RPAREN    -- Right parentheses ')'
        SYMBOL    -- A symbol in the language
        CHARCLASS -- A character class.
    symbol -- If category is SYMBOL, the corresponding symbol (character) for
    this token.
    char_class -- If category is CHARCLASS, a set of symbols in the language.

    """

    EOF = 0
    EOL = 1
    STAR = 2
    PLUS = 3
    PIPE = 4
    LPAREN = 5
    RPAREN = 6
    SYMBOL = 7
    CHARCLASS = 8

    _category_to_str = {
        EOF: "EOF",
        EOL: "EOL",
        STAR: "STAR",
        PLUS: "PLUS",
        PIPE: "PIPE",
        LPAREN: "LPAREN",
        RPAREN: "RPAREN",
        SYMBOL: "SYMBOL",
    }

    def __init__(self, category, arg=None):
        """Create a new token.

        Arguments:
        category -- The syntactic category of this token.
        arg -- If category is SYMBOL, a character. If category is CHARCLASS, a
        collection of characters. Ignored otherwise.

        """
        self.category = category
        if self.category == Token.SYMBOL:
            assert len(arg) == 1 and arg in SIGMA
            self.symbol = arg
        elif self.category == Token.CHARCLASS:
            assert len(arg) >= 1 and all(c in SIGMA for c in arg)
            self.char_class = set(arg)

    def is_end(self):
        """Return whether this token is either an EOF or EOL token."""

        return self.category == Token.EOF or self.category == Token.EOL

    def __repr__(self):
        if self.category == Token.SYMBOL:
            return 'Token(SYMBOL, {})'.format(repr(self.symbol))
        elif self.category == Token.CHARCLASS:
            return 'Token(CHARCLASS, {})'.format(repr(self.char_class))
        else:
            return 'Token({})'.format(self._category_to_str[self.category])

    def __str__(self):
        if self.category == Token.SYMBOL:
            return 'SYMBOL({})'.format(repr(self.symbol))
        elif self.category == Token.CHARCLASS:
            return 'CHARCLASS({})'.format(repr(self.char_class))
        else:
            return self._category_to_str[self.category]
