"""Generic finite automaton class."""

import sys


class Automaton:
    """A finite automaton (a.k.a. finite state machine).

    States which can be reached from the initial state should not be modified
    once the automaton in constructed.

    Attributes:
    initial -- The initial state of this automaton.
    num_states -- The number of states in this automaton.

    """

    def __init__(self, initial):
        """Create a new automaton with the given initial state.

        Arguments:
        initial -- The initial automaton state.

        """

        self.initial = initial
        self.num_states = self._number_states(self.initial, 0)

    def _number_states(self, state, next_number):
        """Number the given state and all states reachable from it.

        Arguments:
        state -- The state to start with. If it does not already have a number,
        it will be assigned next_number.
        next_number -- The number from which to start assigning numbers.

        Returns:
        The largest number that was assigned, plus one.

        """

        if state.number is None:
            state.number = next_number
            next_number += 1
            for (symbol, target) in state._all_transitions():
                next_number = self._number_states(target, next_number)
        return next_number

    def print_graphviz(self, file=sys.stdout):
        """Print automaton for Graphviz dot rendering."""

        print('digraph {} {{'.format(type(self).__name__), file=file)
        print('    rankdir = LR;', file=file)
        print('    I [style = invis];', file=file)

        print('    I -> S{};'.format(self.initial.number), file=file)
        self.initial._print_graphviz(file, set())

        print('}', file=file)


class AutomatonState:
    """A state in a finite automaton storing a set of transitions to other
    states.

    Attributes:
    accepting -- If this state is an accepting state, a positive integer ID
    representing the rule that this accepts; otherwise None.
    transitions -- A set of outgoing transitions from this state represented
    as a dictionary with character keys. The values depend on the type of
    automaton (deterministic vs nondeterministic).
    number -- If this state is in an automaton, a non-negative integer unique
    within the automaton, otherwise None.

    """

    def __init__(self, accepting=None):
        """Create a new state with no transitions."""

        self.accepting = accepting
        self.transitions = {}
        self.number = None

    def _all_transitions(self):
        """Return a flat set of all transitions from this set."""

        raise NotImplementedError

    def _ensure_not_numbered(self):
        if self.number is not None:
            raise ValueError('cannot modify state in automaton')

    def add_transition(self, symbol, to):
        """Add a transition to this state.

        Arguments:
        symbol -- The symbol (character) on which to take the transition.
        to -- The state to transition to on the given symbol.

        """

        raise NotImplementedError

    def _print_graphviz(self, file, seen):
        if self in seen:
            return
        seen.add(self)

        if self.accepting:
            subscript = '{},{}'.format(self.number, self.accepting)
        else:
            subscript = self.number

        print('    S{} [label = <s<sub>{}</sub>>, shape = circle'.format(self.number, subscript),
              file=file, end='')

        if self.accepting:
            print(', peripheries = 2', file=file, end='')
        print('];', file=file)

        for (symbol, target) in self._all_transitions():
            target._print_graphviz(file, seen)
            if symbol is None:
                label = '\u03b5'  # Lower case epsilon
            else:
                label = repr(symbol).replace('\\', '\\\\')  # Escape slashes
            print('    S{} -> S{} [label = "{}"];'.format(self.number, target.number, label),
                  file=file)
