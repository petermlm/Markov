import unittest
from unittest.mock import patch

import markov


class TokenizeTests(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(markov.tokenize('simple'), ['simple'])
        self.assertEqual(markov.tokenize('  simple  '), ['simple'])
        self.assertEqual(markov.tokenize('SiMpLe'), ['simple'])
        self.assertEqual(markov.tokenize('two words'), ['two', 'words'])
        self.assertEqual(markov.tokenize('one more word'), ['one', 'more', 'word'])

    def test_special(self):
        for char in markov.special_chars:
            word = 'abc{}xyz'.format(char)
            self.assertEqual(markov.tokenize(word), ['abc', char, 'xyz'])

    def test_ignored(self):
        for char in markov.ignored_chars:
            word = 'abc{}xyz'.format(char)
            self.assertEqual(markov.tokenize(word), ['abc', 'xyz'])


@patch('markov.make_network')
@patch('markov.make_random_text')
class MarkovTests(unittest.TestCase):
    def test_simple(self, make_random_text_mock, make_network_mock):
        return_value = 'a1', 'a2'
        make_network_mock.return_value = return_value

        text_arg = 'text_arg'
        words_num = 100
        markov.markov(text_arg)

        make_network_mock.assert_called_once_with(text_arg)
        args = return_value + (words_num,)
        make_random_text_mock.assert_called_once_with(*args)

    def test_with_word_nums(self, make_random_text_mock, make_network_mock):
        return_value = 'a1', 'a2'
        make_network_mock.return_value = return_value

        text_arg = 'text_arg'
        words_num = 50
        markov.markov(text_arg, words_num)

        make_network_mock.assert_called_once_with(text_arg)
        args = return_value + (words_num,)
        make_random_text_mock.assert_called_once_with(*args)


if __name__ == '__main__':
    unittest.main()
