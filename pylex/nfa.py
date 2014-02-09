"""Nondeterministic finite automaton class."""

from pylex.automaton import Automaton, AutomatonState


class NFA(Automaton):
    """A nondeterministic finite automaton.

    Each state can have multiple transitions on a single symbol as well as
    transitions without consuming any input (so-called epsilon transitions).

    """

    def __init__(self, initial):
        super().__init__(initial)

    def to_dfa(self):
        """Convert this NFA to an equivalent DFA."""

        from pylex.rabinscott import RabinScott
        return RabinScott(self)()


class NFAState(AutomatonState):
    """A state in a nondeterministic finite automaton.

    Attributes:
    transitions -- A set of outgoing transitions from this state represented as
    a dictionary from characters or None (representing epsilon) to a set of
    states.

    """

    def __init__(self, accepting=None):
        super().__init__(accepting)

    def _all_transitions(self):
        transitions = set()
        for symbol, targets in self.transitions.items():
            transitions |= {(symbol, target) for target in targets}
        return transitions

    def add_transition(self, symbol, to):
        """Add a transition to this state.

        Arguments:
        symbol -- The symbol on which to take the transition; can also be None
        to represent epsilon.
        to -- The state to transition to on the given symbol.

        >>> state1 = NFAState()
        >>> state2 = NFAState()
        >>> state1.add_transition(None, state2)
        >>> state1.add_transition(None, state2)
        >>> len(state1.transitions[None])
        1
        >>> state1.add_transition(None, state1)
        >>> len(state1.transitions[None])
        2
        """

        try:
            # Invalidate the memoized epsilon closure
            del self._epsilon_closure
        except AttributeError:
            pass

        try:
            self.transitions[symbol].add(to)
        except KeyError:
            self.transitions[symbol] = {to}

    def epsilon_closure(self):
        """Compute the epsilon closure for this state.

        The epsilon closure is the set of all states reachable from this state
        in zero or more epsilon transitions.

        >>> state1 = NFAState()
        >>> state2 = NFAState()
        >>> state3 = NFAState()
        >>> state1.add_transition(None, state2)
        >>> state2.add_transition(None, state3)
        >>> state1.epsilon_closure() == {state1, state2, state3}
        True
        >>> state3.add_transition(None, state1) # Cycle
        >>> state1.epsilon_closure() == {state1, state2, state3}
        True
        """

        try:
            return self._epsilon_closure
        except AttributeError:
            epsilon_closure = {self}

            worklist = [self]
            while worklist:
                state = worklist.pop()
                for target in state.transitions.get(None, set()):
                    if target not in epsilon_closure:
                        epsilon_closure.add(target)
                        worklist.append(target)

            self._epsilon_closure = frozenset(epsilon_closure)
            return self._epsilon_closure
