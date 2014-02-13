pylex
=====

`pylex` is a pedagogical scanner generator written in Python 3. It implements
several algorithms related to regular expressions and finite automata,
including:

 * Thompson's construction: convert a regular expression to a nondeterministic
  finite automaton (NFA).
 * Rabin-Scott subset construction (a.k.a. powerset construction): convert an
   NFA to a deterministic finite automaton (DFA).
 * Hopcroft's algorithm: minimize a DFA.
 * Table-driven scanning: simple DFA emulation technique.

The algorithm implementations are straightforward and easy to read rather than
optimized. Intermediate results are saved and can be saved.

Usage
-----

The default behavior for `pylex.py` is to read a list of regular expressions
and convert them to C source code which scans the specified regular language.
Each regular expression in the list appears on its own line; each line
corresponds to a separate syntactic category.

The regular expression syntax is very minimal: it only includes grouping
(`(``)`), the Kleene closure (`*`), the positive closure (`+`), concatenation,
and alternation/union (`|`).

Flags can be passed to capture intermediate stages of the regular expression
compilation; see `pylex --help` for details. Intermediate finite automata can
be printed in Graphviz DOT language for rendering.

Generated Scanner
-----------------

The generated C scanner contains one public function, `pylex`, which is
documented in `pylex/scangen.py`. An example client driver is available in the
`examples` directory. Just run `pylex -c examples/pylex.c` to generate the
scanner and run `make` in the `examples` directory.
