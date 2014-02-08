"""Deterministic finite automaton class."""

from pylex import SIGMA
from pylex.automaton import Automaton, AutomatonState


class DFA(Automaton):
    """A deterministic finite automaton.

    Each state has only a single transition for each symbol and epsilon
    transitions are not allowed.

    """

    def __init__(self, initial):
        super().__init__(initial)

    def minimized(self):
        """Return a minimized DFA equivalent to this DFA."""

        return self._hopcroft()

    def _hopcroft(self):
        """Hopcroft's algorithm: minimize a DFA."""

        T = self._initial_partition()
        P = set()
        
        while P != T:
            P = T
            T = set()

            for p in P:
                T |= DFA._split(p)

        dfa_states = {}
        def aux(subset):
            state = next(iter(subset))
            dfa_state = DFAState(state.accepting)
            dfa_states[subset] = dfa_state

            for (symbol, target) in state.transitions.items():
                target_subset = next(p for p in P if target in p)

                if target_subset not in dfa_states:
                    aux(target_subset)
                dfa_state.add_transition(symbol, dfa_states[target_subset])

            return dfa_state

        initial_subset = next(p for p in P if self.initial in p)

        return DFA(aux(initial_subset))

    def _initial_partition(self):
        """Perform an initial partition of all of the states of this DFA based
        on their accepting behavior.

        """

        from collections import defaultdict

        T = defaultdict(lambda: set())
        def aux(state):
            T[state.accepting].add(state)
            for target in state.transitions.values():
                if target not in set.union(*T.values()):
                    aux(target)
        aux(self.initial)

        return set(frozenset(s) for s in T.values())

    @staticmethod
    def _split(S):
        def splits(c):
            for i in S:
                s1 = set()
                s2 = set()

                expected = i.transitions.get(c, None)
                for j in S:
                    actual = j.transitions.get(c, None)
                    if actual == expected:
                        s1.add(j)
                    else:
                        s2.add(j)
                
                if s1 and s2:
                    return {frozenset(s1), frozenset(s2)}

        for c in SIGMA:
            split = splits(c)
            if split:
                return split
        else:
            return {S}

class DFAState(AutomatonState):
    """A state in a deterministic finite automaton.

    Attributes:
    transitions -- A set of outgoing transitions from this state represented as
    a dictionary from characters to another state.
    
    """

    def __init__(self, accepting=None):
        super().__init__(accepting)

    def _all_transitions(self):
        return set(self.transitions.items())

    def add_transition(self, symbol, to):
        """Add a transition to this state. 

        Arguments:
        symbol -- The symbol on which to take the transition; must not already
        be in the keys of transitions and must not be None.
        to -- The state to transition to on the given symbol.

        >>> state1 = DFAState()
        >>> state2 = DFAState()
        >>> state1.add_transition('a', state2)
        >>> state1.add_transition('b', state1)
        >>> len(state1.transitions)
        2
        >>> state1.add_transition(None, state2)
        Traceback (most recent call last):
            ...
        AssertionError: DFA cannot contain epsilon transitions
        >>> state1.add_transition('a', state2)
        Traceback (most recent call last):
            ...
        AssertionError: state already contains given transition
        """

        assert symbol is not None, 'DFA cannot contain epsilon transitions'
        assert symbol not in self.transitions, 'state already contains given transition'
        self.transitions[symbol] = to
