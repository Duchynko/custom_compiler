import unittest
from unittest.mock import patch, mock_open
from scanner import Scanner, SourceFile
from tokens import Kind


class TestScanner(unittest.TestCase):
    def test_init(self):
        with patch('builtins.open', mock_open(read_data='Hello')):
            scanner = Scanner('')

            self.assertEqual(scanner.current_char, 'H')
            self.assertEqual(scanner.current_spelling, [])

    def test_take_it_one(self):
        with patch('builtins.open', mock_open(read_data='Hello')):
            scanner = Scanner('')

            scanner.take_it()

            self.assertEqual(scanner.current_char, 'e')
            self.assertEqual(scanner.current_spelling, ['H'])

    def test_take_it_multiple(self):
        with patch('builtins.open', mock_open(read_data='Hello')):
            scanner = Scanner('')

            scanner.take_it()
            scanner.take_it()
            scanner.take_it()

            self.assertEqual(scanner.current_char, 'l')
            self.assertEqual(scanner.current_spelling, ['H', 'e', 'l'])

    def test_discard_separator_space_go_to_next_character(self):
        with patch('builtins.open', mock_open(read_data=' Hello')):
            scanner = Scanner('')

            scanner.discard_separator()

            self.assertEqual(scanner.current_spelling, [' '])
            self.assertEqual(scanner.current_char, 'H')

    def test_discard_separator_newline_go_to_next_character(self):
        with patch('builtins.open', mock_open(read_data='\nHello')):
            scanner = Scanner('')

            scanner.discard_separator()

            self.assertEqual(scanner.current_spelling, ['\n'])
            self.assertEqual(scanner.current_char, 'H')

    def test_discard_separator_comment_discared_goes_to_new_line(self):
        with patch('builtins.open', mock_open(read_data='# Comment\nHello')):
            scanner = Scanner('')

            scanner.discard_separator()

            self.assertEqual(''.join(scanner.current_spelling), '# Comment\n')

    def test_scan_token_only_letters_return_identifier(self):
        with patch('builtins.open', mock_open(read_data='Hello World')):
            scanner = Scanner('')

            token_type = scanner.scan_token()

            self.assertEqual(token_type, Kind.IDENTIFIER)
            self.assertEqual(''.join(scanner.current_spelling), 'Hello')

    def test_scan_token_letters_and_digits_return_identifier(self):
        with patch('builtins.open', mock_open(read_data='H3ll0')):
            scanner = Scanner('')

            token_type = scanner.scan_token()

            self.assertEqual(token_type, Kind.IDENTIFIER)

    def test_scan_token_return_error_if_not_found(self):
        with patch('builtins.open', mock_open(read_data='_Hello')):
            scanner = Scanner('')

            token = scanner.scan_token()

            self.assertEqual(token, Kind.ERROR)

    def test_scan_token_digits_return_int_literal(self):
        with patch('builtins.open', mock_open(read_data='123')):
            scanner = Scanner('')

            token_type = scanner.scan_token()

            self.assertEqual(token_type, Kind.INTEGER_LITERAL)
            self.assertEqual(''.join(scanner.current_spelling), '123')

    def test_scan_token_digits_return_eot_empty_file(self):
        with patch('builtins.open', mock_open(read_data='')):
            scanner = Scanner('')

            token_type = scanner.scan_token()

            self.assertEqual(token_type, Kind.EOT)

    def test_scan_token_operators_return_operator(self):
        with patch('builtins.open', mock_open(read_data='*')):
            scanner = Scanner('')

            token_type = scanner.scan_token()

            self.assertEqual(token_type, Kind.OPERATOR)
            scanner.source.source.close()


class TestSourceFile(unittest.TestCase):
    def test_init(self):
        file = SourceFile('../example_files/testfile.txt')

        self.assertEqual(file.source.name, '../example_files/testfile.txt')
        file.source.close()

    def test_init_exit_if_file_dont_exist(self):
        with self.assertRaises(SystemExit):
            SourceFile('xxx')

    def test_get_next_char_get_one(self):
        with patch("builtins.open", mock_open(read_data="Hello")):
            file = SourceFile('')
            char = file.get_next_char()

            self.assertEqual(char, 'H')

    def test_get_next_char_returns_eot_in_empty_file(self):
        with patch("builtins.open", mock_open(read_data="")):
            file = SourceFile('')
            char = file.get_next_char()

            self.assertEqual(char, file.EOT)

    def test_get_next_char_returns_eot_at_the_end_of_file(self):
        with patch("builtins.open", mock_open(read_data="")):
            file = SourceFile('')
            char = file.get_next_char()

            self.assertEqual(char, file.EOT)

    def test_get_next_char_get_many(self):
        with patch("builtins.open", mock_open(read_data="Hello")):
            file = SourceFile('')
            char_h = file.get_next_char()
            char_e = file.get_next_char()
            char_l = file.get_next_char()

            self.assertEqual(char_h, 'H')
            self.assertEqual(char_e, 'e')
            self.assertEqual(char_l, 'l')
