"""Main pylex driver program."""

import argparse
import doctest
import sys

from pylex.ast import asts_to_nfa
from pylex.parser import Parser
from pylex.scanner import Scanner


def main():
    parser = argparse.ArgumentParser(description='Generate programs for scanning of text.')

    parser.add_argument('-l', '--lex', type=argparse.FileType('w'), metavar='FILE',
                        help='emit a log of lexed tokens to a specified file')
    parser.add_argument('-a', '--ast', type=argparse.FileType('w'), metavar='FILE',
                        help='emit the parsed regex ASTs to a specified file')
    parser.add_argument('-n', '--nfa', type=argparse.FileType('w'),
                        metavar='FILE', default=sys.stdout,
                        help='write the NFA for Graphviz dot rendering')

    args = parser.parse_args()

    scanner = Scanner(sys.stdin, args.lex)
    parser = Parser(scanner)

    asts = parser.parse_top_level()
    for ast in asts:
        if args.ast:
            print(ast, file=args.ast)

    nfa = asts_to_nfa(asts)
    nfa.print_graphviz(args.nfa)

    scanner.close()

if __name__ == '__main__':
    main()
