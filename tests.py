import unittest
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


if __name__ == '__main__':
    unittest.main()
