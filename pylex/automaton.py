"""Generic finite automaton class."""

import sys


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

    def print_graphviz(self, file=sys.stdout):
        """Print automaton for Graphviz dot rendering."""

        print('digraph {} {{'.format(type(self).__name__), file=file)
        print('    rankdir = LR;', file=file)
        print('    I [style = invis];', file=file)

        print('    I -> S0;', file=file)
        self.initial._print_graphviz(file, {})

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
    
    """

    def __init__(self, accepting=None):
        """Create a new state with no transitions."""

        self.accepting = accepting
        self.transitions = {}

    def _all_transitions(self):
        """Return a flat set of all transitions from this set."""

        raise NotImplementedError

    def add_transition(self, symbol, to):
        """Add a transition to this state.

        Arguments:
        symbol -- The symbol (character) on which to take the transition.
        to -- The state to transition to on the given symbol.

        """

        raise NotImplementedError

    def _print_graphviz(self, file, seen):
        if self not in seen:
            seen[self] = len(seen)
        index = seen[self]

        if self.accepting:
            subscript = '{},{}'.format(index, self.accepting)
        else:
            subscript = index

        print('    S{} [label = <s<sub>{}</sub>>, shape = circle'.format(index, subscript),
              file=file, end='')

        if self.accepting:
            print(', peripheries = 2', file=file, end='')
        print('];', file=file)

        for (symbol, target) in self._all_transitions():
            if target not in seen:
                target._print_graphviz(file, seen)
            target_index = seen[target]

            if symbol is None:
                symbol = '\u03b5'
            print('    S{} -> S{} [label = "{}"];'.format(index, target_index, symbol),
                  file=file)
