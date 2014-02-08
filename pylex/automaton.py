"""Generic finite automaton class."""

class Automaton:
    """A finite automaton (a.k.a. finite state machine).

    Attributes:
    initial -- The initial state of this automaton.

    """

    def __init__(self, initial):
        """Create a new automaton with the given initial state.

        Arguments:
        initial -- The initial automaton state.

        """

        self.initial = initial

class AutomatonState:
    """
    A state in a finite automaton storing a set of transitions to other
    states.

    Attributes:
    accepting -- If this state is an accepting state, a positive integer ID
    representing the rule that this accepts; otherwise None.
    transitions -- A set of outgoing transitions from this state represented
    as a dictionary with character keys. The values depend on the type of
    automaton (deterministic vs nondeterministic).
    
    """

    def __init__(self, accepting=None):
        """Create a new state with no transitions."""

        self.accepting = accepting
        self.transitions = {}

    def add_transition(self, symbol, to):
        """Add a transition to this state.

        Arguments:
        symbol -- The symbol (character) on which to take the transition.
        to -- The state to transition to on the given symbol.

        """

        raise NotImplementedError
