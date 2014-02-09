"""Implementation of Hopcroft's algorithm."""

from pylex import SIGMA
from pylex.dfa import DFA, DFAState


class Hopcroft:
    """Hopcroft's algorithm: minimize a DFA."""

    def __init__(self, dfa):
        """Create a DFA minimizer for the given DFA."""

        self.initial = dfa.initial

    def __call__(self):
        T = self._initial_partition()
        self.P = set()

        # Iterate until a fixed point.
        while self.P != T:
            self.P = T
            T = set()

            for p in self.P:
                T |= self._split(p)

        dfa_states = {}

        def aux(subset):
            state = next(iter(subset))
            dfa_state = DFAState(state.accepting)
            dfa_states[subset] = dfa_state

            for (symbol, target) in state.transitions.items():
                target_subset = self._partition_containing(target)

                if target_subset not in dfa_states:
                    aux(target_subset)
                dfa_state.add_transition(symbol, dfa_states[target_subset])

            return dfa_state

        initial_subset = self._partition_containing(self.initial)

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

    def _split(self, S):
        """Attempt to split a set of DFA states based on their transitions to
        other subsets in the partition.

        """

        def splits(c):
            for i in S:
                s1 = set()
                s2 = set()

                expected = i.transitions.get(c, None)
                expected = self._partition_containing(expected)
                for j in S:
                    actual = j.transitions.get(c, None)
                    actual = self._partition_containing(actual)
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

    def _partition_containing(self, state):
        try:
            return next(p for p in self.P if state in p)
        except StopIteration:
            return None
