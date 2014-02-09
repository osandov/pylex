"""Implementation of the Rabin-Scott subset construction (a.k.a powerset
construction).

"""

from pylex import SIGMA
from pylex.dfa import DFA, DFAState
from pylex.nfa import NFA, NFAState


class RabinScott:
    """Rabin-Scott powerset construction: convert this NFA to an equivalent
    DFA.

    """

    def __init__(self, nfa):
        """Create an NFA to DFA converter for the given NFA."""

        self.initial = nfa.initial

    def __call__(self):
        # Initial configuration
        q0 = self.initial.epsilon_closure()

        # Map from known configuration to corresponding DFA state
        Q = {q0: self._configuration_to_dfa_state(q0)}

        worklist = [q0]
        while worklist:
            q = worklist.pop()

            for symbol in SIGMA:
                t = self._delta_closure(q, symbol)

                if t:
                    try:
                        dfa_state = Q[t]
                    except KeyError:
                        dfa_state = self._configuration_to_dfa_state(t)
                        Q[t] = dfa_state
                        worklist.append(t)

                    Q[q].add_transition(symbol, dfa_state)

        return DFA(Q[q0])

    def _delta_closure(self, q, c):
        """Return EpsilonClosure(Delta(q, c))."""

        delta_closure = set()
        for state in q:
            for target in state.transitions.get(c, set()):
                delta_closure |= target.epsilon_closure()

        return frozenset(delta_closure)

    def _configuration_to_dfa_state(self, q):
        """Create a DFA state from the given configuration.

        If the configuration contains any accepting states, the DFA will have
        the minimum accepting ID in the category. This ensure that we match the
        first rule to accept a string. If the configuration doesn't contain any
        accepting states, the DFA state will not be an accepting state.

        """

        try:
            accepting = min(state.accepting for state in q if state.accepting)
        except ValueError:
            accepting = None

        return DFAState(accepting)
