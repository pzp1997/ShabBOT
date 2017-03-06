from .context import shabbot

import types
import unittest


class TestNormalizeFrequency(unittest.TestCase):

    def test_returns_generator(self):
        self.assertIs(types.GeneratorType, type(shabbot.normalize_freq([])))

    def test_empty_list(self):
        self.assertEqual([], list(shabbot.normalize_freq([])))

    def test_uniform_probability(self):
        self.assertEqual([0.2] * 5, list(shabbot.normalize_freq([1] * 5)))

    def test_non_uniform_probability(self):
        self.assertEqual([0.1, 0.6, 0.3],
                         list(shabbot.normalize_freq([2, 12, 6])))


if __name__ == '__main__':
    unittest.main()
