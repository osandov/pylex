"""Abstract syntax tree class."""


class AST:
    """Node in a regular expression abstract syntax tree."""

    pass


class SymbolAST(AST):
    """AST leaf node: symbol in the alphabet.

    Attributes:
    symbol -- The symbol for this node.

    """

    def __init__(self, symbol):
        """Create a new symbol AST node.

        Arguments:
        symbol -- The symbol (character) for this node.

        """

        super().__init__()
        self.symbol = symbol

    def __repr__(self):
        return 'SymbolAST({})'.format(repr(self.symbol))


class KleeneAST(AST):
    """AST node for the Kleene star operator.

    Attributes:
    operand -- Operand of the closure.

    """

    def __init__(self, operand):
        """Create a new Kleene closure AST node.

        Arguments:
        operand -- AST operand of the closure.

        """

        super().__init__()
        self.operand = operand

    def __repr__(self):
        return 'KleeneAST({})'.format(repr(self.operand))


class AlternationAST(AST):
    """Alternation (a.k.a. union) of two regular expressions.

    Attributes:
    lhs -- The left-hand side of the operator.
    rhs -- The right-hand side of the operator.

    """

    def __init__(self, lhs, rhs):
        """Create a new alternation AST node.

        Arguments:
        lhs -- Left-hand side AST.
        rhs -- Right-hand side AST.

        """

        super().__init__()
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        return 'AlternationAST({}, {})'.format(repr(self.lhs), repr(self.rhs))


class ConcatenationAST(AST):
    """Concatenation of two regular expressions.

    Attributes:
    lhs -- The left-hand side of the operator.
    rhs -- The right-hand side of the operator.

    """

    def __init__(self, lhs, rhs):
        """Create a new concatenation AST node.

        Arguments:
        lhs -- Left-hand side AST.
        rhs -- Right-hand side AST.

        """

        super().__init__()
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        return 'ConcatenationAST({}, {})'.format(repr(self.lhs), repr(self.rhs))
