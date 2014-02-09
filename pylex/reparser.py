"""Syntactic analysis phase of the regular expression compiler."""

from pylex.ast import SymbolAST, KleeneAST, AlternationAST, ConcatenationAST
from pylex.rescanner import RegexScanner
from pylex.token import Token


class ParsingError(Exception):
    """Error encountered while parsing."""

    pass


class RegexParser:
    """A regular expression parser."""

    def __init__(self, scanner):
        """Create a new parser over a scanner.

        Arguments:
        scanner -- The scanner from which to read tokens.

        """

        self._scanner = scanner

    def _consume_token(self):
        """Lex a token from the scanner."""

        self._current_token = self._scanner.lex()

    def parse_top_level(self):
        """Parse a top-level newline-delimited list of regular expressions.

        Returns:
        A list of ASTs.

        Raises:
        ParsingError -- If an error was encountered parsing the input.

        >>> RegexParser(RegexScanner('')).parse_top_level()
        []
        >>> RegexParser(RegexScanner('\\n\\n')).parse_top_level()
        []
        >>> RegexParser(RegexScanner('A\\n((B))\\nC*')).parse_top_level()
        [SymbolAST('A'), SymbolAST('B'), KleeneAST(SymbolAST('C'))]
        >>> RegexParser(RegexScanner('XYZ*')).parse_top_level()
        [ConcatenationAST(SymbolAST('X'), ConcatenationAST(SymbolAST('Y'), KleeneAST(SymbolAST('Z'))))]
        >>> RegexParser(RegexScanner('P|Q|R')).parse_top_level()
        [AlternationAST(SymbolAST('P'), AlternationAST(SymbolAST('Q'), SymbolAST('R')))]
        >>> RegexParser(RegexScanner('ab|c')).parse_top_level()
        [AlternationAST(ConcatenationAST(SymbolAST('a'), SymbolAST('b')), SymbolAST('c'))]
        >>> RegexParser(RegexScanner('(A')).parse_top_level()
        Traceback (most recent call last):
            ...
        reparser.ParsingError: unmatched parentheses
        >>> RegexParser(RegexScanner('()')).parse_top_level()
        Traceback (most recent call last):
            ...
        reparser.ParsingError: expected regex term
        >>> RegexParser(RegexScanner('O**')).parse_top_level()
        Traceback (most recent call last):
            ...
        reparser.ParsingError: junk after regex
        """

        asts = []

        # Prime the lexer.
        self._consume_token()

        while self._current_token.category != Token.EOF:
            # Ignore empty line.
            if self._current_token.category != Token.EOL:
                ast = self._parse_regex()

                if not self._current_token.is_end():
                    raise ParsingError('junk after regex')

                asts.append(ast)

            # Eat the EOL.
            self._consume_token()

        return asts

    def _parse_regex(self):
        """<regex> ::= <alternation>"""
        return self._parse_alternation()

    def _parse_term(self):
        """<term> ::= symbol | <parenthetical>"""

        if self._current_token.category == Token.SYMBOL:
            ast = SymbolAST(self._current_token.symbol)
            # Eat the symbol.
            self._consume_token()
            return ast
        elif self._current_token.category == Token.LPAREN:
            return self._parse_parenthetical()
        else:
            raise ParsingError('expected regex term')

    def _parse_parenthetical(self):
        """<parenthetical> ::= '(' <regex> ')'"""

        assert self._current_token.category == Token.LPAREN
        # Eat the opening paren.
        self._consume_token()

        ast = self._parse_regex()

        if self._current_token.category != Token.RPAREN:
            raise ParsingError('unmatched parentheses')

        # Eat the closing paren.
        self._consume_token()

        return ast

    def _parse_kleene(self):
        """<kleene> ::= <term> | <term> '*'"""

        ast = self._parse_term()

        if self._current_token.category == Token.STAR:
            ast = KleeneAST(ast)
            # Eat the asterisk.
            self._consume_token()

        return ast

    def _parse_concatenation(self):
        """<concatenation> ::= <kleene> | <kleene> <concatenation>"""

        lhs = self._parse_kleene()

        if self._current_token.category in [Token.SYMBOL, Token.LPAREN]:
            rhs = self._parse_concatenation()
            return ConcatenationAST(lhs, rhs)
        else:
            # There is no valid right-hand side, return what we got.
            return lhs

    def _parse_alternation(self):
        """<alternation> ::= <concatenation> | <concatenation> '|' <alternation>"""

        lhs = self._parse_concatenation()

        if self._current_token.category == Token.PIPE:
            # Eat the pipe.
            self._consume_token()
            rhs = self._parse_alternation()
            return AlternationAST(lhs, rhs)
        else:
            # There is no valid right-hand side, return what we got.
            return lhs
