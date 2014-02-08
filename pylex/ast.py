"""Abstract syntax tree class."""

from pylex.nfa import NFA, NFAState


class AST:
    """Node in a regular expression abstract syntax tree."""

    def to_nfa(self, accepting_id=1):
        """Convert this AST to an NFA.

        Arguments:
        accepting_id -- The ID of the accepting state. Defaults to 1.

        """

        (initial, accepting) = self._thompson()
        accepting.accepting = accepting_id
        return NFA(initial)

    def _thompson(self):
        """
        Thompson's construction: convert this AST to an NFA.

        The temporary representation of the NFA is an (initial state, accepting
        state) tuple. The accepting state's ID is None.

        """

        raise NotImplementedError


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

    def _thompson(self):
        initial = NFAState()
        accepting = NFAState()
        initial.add_transition(self.symbol, accepting)
        return (initial, accepting)

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

    def _thompson(self):
        initial = NFAState()
        accepting = NFAState()

        (oinitial, oaccepting) = self.operand._thompson()

        initial.add_transition(None, oinitial)
        oaccepting.add_transition(None, accepting)

        oaccepting.add_transition(None, oinitial)
        initial.add_transition(None, accepting)

        return (initial, accepting)

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

    def _thompson(self):
        initial = NFAState()
        accepting = NFAState()

        (linitial, laccepting) = self.lhs._thompson()
        (rinitial, raccepting) = self.rhs._thompson()

        initial.add_transition(None, linitial)
        initial.add_transition(None, rinitial)

        laccepting.add_transition(None, accepting)
        raccepting.add_transition(None, accepting)

        return (initial, accepting)

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

    def _thompson(self):
        (linitial, laccepting) = self.lhs._thompson()
        (rinitial, raccepting) = self.rhs._thompson()

        laccepting.add_transition(None, rinitial)

        return (linitial, raccepting)

    def __repr__(self):
        return 'ConcatenationAST({}, {})'.format(repr(self.lhs), repr(self.rhs))


def asts_to_nfa(asts):
    """Convert a list of ASTs to an NFA.

    Thompson's construction is applied to each AST and an initial state is
    created with epsilon transitions to the initial transitions of each
    constructed NFA. The accepting states are given unique IDs ascending from 1
    in the original order of the list.

    """

    initial = NFAState()

    for i, ast in enumerate(asts, 1):
        (ainitial, aaccepting) = ast._thompson()
        aaccepting.accepting = i
        initial.add_transition(None, ainitial)

    return NFA(initial)
