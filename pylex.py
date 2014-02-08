"""Main pylex driver program."""

import argparse
import doctest
import sys

from pylex.scanner import Scanner
from pylex.token import Token


def main():
    parser = argparse.ArgumentParser(
        description='Generate programs for scanning of text.')

    parser.add_argument('-l', '--lex', type=argparse.FileType('w'),
                        metavar='FILE', default=sys.stdout,
                        help='emit a log of lexed tokens to a specified file')

    args = parser.parse_args()

    scanner = Scanner(sys.stdin, args.lex)
    while scanner.lex().category != Token.EOF:
        pass
    scanner.close()

if __name__ == '__main__':
    main()
