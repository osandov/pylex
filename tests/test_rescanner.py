import unittest

from pylex.rescanner import RegexScanner, ScanningError
from pylex.token import Token

class TestRegexScanner(unittest.TestCase):
    def test_eof(self):
        scanner = RegexScanner('')
        self.assertEqual(scanner.lex().category, Token.EOF)

        # Repeated calls after we hit the end should still yield EOF.
        self.assertEqual(scanner.lex().category, Token.EOF)
        self.assertEqual(scanner.lex().category, Token.EOF)

    def test_eol(self):
        scanner = RegexScanner('\n\n')
        self.assertEqual(scanner.lex().category, Token.EOL)
        self.assertEqual(scanner.lex().category, Token.EOL)
        self.assertEqual(scanner.lex().category, Token.EOF)

    def test_star(self):
        scanner = RegexScanner('*')
        self.assertEqual(scanner.lex().category, Token.STAR)
        self.assertEqual(scanner.lex().category, Token.EOF)

    def test_plus(self):
        scanner = RegexScanner('+')
        self.assertEqual(scanner.lex().category, Token.PLUS)
        self.assertEqual(scanner.lex().category, Token.EOF)

    def test_pipe(self):
        scanner = RegexScanner('|')
        self.assertEqual(scanner.lex().category, Token.PIPE)
        self.assertEqual(scanner.lex().category, Token.EOF)

    def test_parens(self):
        scanner = RegexScanner('(())')
        self.assertEqual(scanner.lex().category, Token.LPAREN)
        self.assertEqual(scanner.lex().category, Token.LPAREN)
        self.assertEqual(scanner.lex().category, Token.RPAREN)
        self.assertEqual(scanner.lex().category, Token.RPAREN)
        self.assertEqual(scanner.lex().category, Token.EOF)

        scanner = RegexScanner(')((()')
        self.assertEqual(scanner.lex().category, Token.RPAREN)
        self.assertEqual(scanner.lex().category, Token.LPAREN)
        self.assertEqual(scanner.lex().category, Token.LPAREN)
        self.assertEqual(scanner.lex().category, Token.LPAREN)
        self.assertEqual(scanner.lex().category, Token.RPAREN)
        self.assertEqual(scanner.lex().category, Token.EOF)

    def test_escape_sequences(self):
        scanner = RegexScanner(r'\0\a\b\t\n\v\f\r\\')
        for c in '\0\a\b\t\n\v\f\r\\':
            token = scanner.lex()
            self.assertEqual(token.category, Token.SYMBOL)
            self.assertEqual(token.symbol, c)
        self.assertEqual(scanner.lex().category, Token.EOF)

    def test_escape_metachars(self):
        scanner = RegexScanner(r'\*\+\|\(\)')
        for c in '*+|()':
            token = scanner.lex()
            self.assertEqual(token.category, Token.SYMBOL)
            self.assertEqual(token.symbol, c)
        self.assertEqual(scanner.lex().category, Token.EOF)

    def test_trailing_backslash(self):
        scanner = RegexScanner('\\')
        with self.assertRaises(ScanningError):
            scanner.lex()
