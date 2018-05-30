# -*- coding: utf-8 -*-

import unittest

from anagrams import find_anagrams


class AnagramsTest(unittest.TestCase):
    def setUp(self):
        self.without_anagrams = ("dog", "cat", "fish", "yellow")
        self.with_anagrams_only = ["caret", "cater", "crate"]
        self.mixed = ["dater", "rated", "trader", "trade",
                      "apple pie", "LIKE", "Work"]
        self.inclusive = ("code", "coed", "deco")

    def test_invalid_word_input(self):
        self.assertRaises(TypeError, find_anagrams, None, self.without_anagrams)

    def test_invalid_word_list_input(self):
        self.assertRaises(TypeError, find_anagrams, "test", None)

    def test_list_with_anagrams_only(self):
        initial_word = "trace"
        anagrams = find_anagrams(initial_word, self.with_anagrams_only)
        self.assertItemsEqual(anagrams, self.with_anagrams_only)

    def test_mixed(self):
        initial_word = "tread"
        anagrams = find_anagrams(initial_word, self.mixed)
        self.assertItemsEqual(anagrams, ["dater", "rated", "trade"])

    def test_wuthout_anagrams(self):
        initial_word = "sky"
        anagrams = find_anagrams(initial_word, self.without_anagrams)
        self.assertItemsEqual(anagrams, [])

    def test_inclusive(self):
        initial_word = "code"
        anagrams = find_anagrams(initial_word, self.inclusive)
        self.assertItemsEqual(anagrams, ["coed", "deco", "code"])

if __name__ == '__main__':
    unittest.main()