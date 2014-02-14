import unittest

from pylex import SIGMA
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

    def test_chars(self):
        scanner = RegexScanner('abc')
        for c in 'abc':
            token = scanner.lex()
            self.assertEqual(token.category, Token.SYMBOL)
            self.assertEqual(token.symbol, c)
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

    def test_simple_char_class(self):
        scanner = RegexScanner('0[abc]')
        scanner.lex()
        token = scanner.lex()
        self.assertEqual(token.category, Token.CHARCLASS)
        self.assertEqual(token.char_class, {'a', 'b', 'c'})

        scanner = RegexScanner('[^abc]')
        token = scanner.lex()
        self.assertEqual(token.category, Token.CHARCLASS)
        self.assertEqual(token.char_class, set(SIGMA) - {'a', 'b', 'c'})

    def test_closing_bracket_in_char_class(self):
        scanner = RegexScanner('[]]')
        token = scanner.lex()
        self.assertEqual(token.category, Token.CHARCLASS)
        self.assertEqual(token.char_class, {']'})

        scanner = RegexScanner('[]3]')
        token = scanner.lex()
        self.assertEqual(token.category, Token.CHARCLASS)
        self.assertEqual(token.char_class, {']', '3'})

        scanner = RegexScanner('[^]]')
        token = scanner.lex()
        self.assertEqual(token.category, Token.CHARCLASS)
        self.assertEqual(token.char_class, set(SIGMA) - {']'})

        scanner = RegexScanner('[^]3]')
        token = scanner.lex()
        self.assertEqual(token.category, Token.CHARCLASS)
        self.assertEqual(token.char_class, set(SIGMA) - {']', '3'})

    def test_char_class_range(self):
        expected = {chr(c) for c in range(ord('a'), ord('z') + 1)}

        scanner = RegexScanner('[a-z]')
        token = scanner.lex()
        self.assertEqual(token.category, Token.CHARCLASS)
        self.assertEqual(token.char_class, expected)

        scanner = RegexScanner('[^a-z]')
        token = scanner.lex()
        self.assertEqual(token.category, Token.CHARCLASS)
        self.assertEqual(token.char_class, set(SIGMA) - expected)

        expected |= {chr(c) for c in range(ord('0'), ord('9') + 1)}

        scanner = RegexScanner('[a-z0-9]')
        token = scanner.lex()
        self.assertEqual(token.category, Token.CHARCLASS)
        self.assertEqual(token.char_class, expected)

        scanner = RegexScanner('[^a-z0-9]')
        token = scanner.lex()
        self.assertEqual(token.category, Token.CHARCLASS)
        self.assertEqual(token.char_class, set(SIGMA) - expected)

    def test_hyphen_in_char_class(self):
        scanner = RegexScanner('[-]')
        token = scanner.lex()
        self.assertEqual(token.category, Token.CHARCLASS)
        self.assertEqual(token.char_class, {'-'})

        scanner = RegexScanner('[^-]')
        token = scanner.lex()
        self.assertEqual(token.category, Token.CHARCLASS)
        self.assertEqual(token.char_class, set(SIGMA) - {'-'})

    def test_hyphen_and_bracket_in_char_class(self):
        scanner = RegexScanner('[]-]')
        token = scanner.lex()
        self.assertEqual(token.category, Token.CHARCLASS)
        self.assertEqual(token.char_class, {']', '-'})

        scanner = RegexScanner('[^]-]')
        token = scanner.lex()
        self.assertEqual(token.category, Token.CHARCLASS)
        self.assertEqual(token.char_class, set(SIGMA) - {']', '-'})

    def test_trailing_hyphen_in_char_class(self):
        scanner = RegexScanner('[a-]')
        token = scanner.lex()
        self.assertEqual(token.category, Token.CHARCLASS)
        self.assertEqual(token.char_class, {'a', '-'})

        scanner = RegexScanner('[-]')
        token = scanner.lex()
        self.assertEqual(token.category, Token.CHARCLASS)
        self.assertEqual(token.char_class, {'-'})

        scanner = RegexScanner('[^a-]')
        token = scanner.lex()
        self.assertEqual(token.category, Token.CHARCLASS)
        self.assertEqual(token.char_class, set(SIGMA) - {'a', '-'})

        scanner = RegexScanner('[^-]')
        token = scanner.lex()
        self.assertEqual(token.category, Token.CHARCLASS)
        self.assertEqual(token.char_class, set(SIGMA) - {'-'})

    def test_unmatched_bracket_in_char_class(self):
        scanner = RegexScanner('[a-')
        with self.assertRaises(ScanningError):
            scanner.lex()

        scanner = RegexScanner('[^a-')
        with self.assertRaises(ScanningError):
            scanner.lex()

    def test_invalid_range_in_char_class(self):
        scanner = RegexScanner('[z-a]')
        with self.assertRaises(ScanningError):
            scanner.lex()

        scanner = RegexScanner('[^z-a]')
        with self.assertRaises(ScanningError):
            scanner.lex()

    def test_caret_in_char_class(self):
        scanner = RegexScanner('[a^]')
        token = scanner.lex()
        self.assertEqual(token.category, Token.CHARCLASS)
        self.assertEqual(token.char_class, {'a', '^'})

        scanner = RegexScanner('[^a^]')
        token = scanner.lex()
        self.assertEqual(token.category, Token.CHARCLASS)
        self.assertEqual(token.char_class, set(SIGMA) - {'a', '^'})

    def test_backslash_in_char_class(self):
        scanner = RegexScanner(r'[\n]')
        token = scanner.lex()
        self.assertEqual(token.category, Token.CHARCLASS)
        self.assertEqual(token.char_class, {'\\', 'n'})

        scanner = RegexScanner(r'[^\n]')
        token = scanner.lex()
        self.assertEqual(token.category, Token.CHARCLASS)
        self.assertEqual(token.char_class, set(SIGMA) - {'\\', 'n'})
