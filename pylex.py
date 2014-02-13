#!/usr/bin/env python3

"""Main pylex driver program."""

import argparse
import doctest
import sys

from pylex.ast import asts_to_nfa
from pylex.reparser import RegexParser
from pylex.rescanner import RegexScanner
from pylex.scangen import TableDrivenScannerGenerator


def main():
    parser = argparse.ArgumentParser(description='Generate programs for scanning of text.')

    parser.add_argument('-l', '--lex', type=argparse.FileType('w'), metavar='FILE',
                        help='emit a log of lexed tokens to a specified file')
    parser.add_argument('-a', '--ast', type=argparse.FileType('w'), metavar='FILE',
                        help='emit the parsed regex ASTs to a specified file')
    parser.add_argument('-n', '--nfa', type=argparse.FileType('w'), metavar='FILE',
                        help='write the NFA for Graphviz dot rendering')
    parser.add_argument('-d', '--dfa', type=argparse.FileType('w'), metavar='FILE',
                        help='write the DFA for Graphviz dot rendering')
    parser.add_argument('-m', '--min-dfa', type=argparse.FileType('w'), metavar='FILE',
                        help='write the minimized DFA for Graphviz dot rendering')
    parser.add_argument('-c', '--c-source', type=argparse.FileType('w'),
                        metavar='FILE', default=sys.stdout,
                        help='write the C source code for a scanner (defaults to stdout)')

    args = parser.parse_args()

    rescanner = RegexScanner(sys.stdin, args.lex)
    reparser = RegexParser(rescanner)

    asts = reparser.parse_top_level()
    for ast in asts:
        if args.ast:
            print(ast, file=args.ast)

    nfa = asts_to_nfa(asts)
    if args.nfa:
        nfa.print_graphviz(args.nfa)

    dfa = nfa.to_dfa()
    if args.dfa:
        dfa.print_graphviz(args.dfa)

    min_dfa = dfa.minimized()
    if args.min_dfa:
        min_dfa.print_graphviz(args.min_dfa)

    scangen = TableDrivenScannerGenerator(min_dfa)
    args.c_source.write(scangen.c_source())

    rescanner.close()

if __name__ == '__main__':
    main()
