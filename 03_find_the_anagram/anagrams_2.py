# -*- coding: utf-8 -*-

from logger import configure_logger

logging = configure_logger(filename="anagrams2.log",
                           logger_name="anagrams2")


def find_anagrams_2(word, word_list):
    """Find all anagrams for given word in iterable.
       To ignore anagram mismatch possibility, all
       words are converted to lowercase.

    Args:
        word (str): initial word to find anagrams for.
        word_list (tuple<str>, list<str>): an iterable of words for comparison.

    Returns:
        list<str>: list of anagrams for given word.

    Exception:
        TypeError: If word is not of type str.
        TypeError: If word_list is not list or tuple.
    """

    if not isinstance(word, str):
        logging.error("Invalid arg for param 'word': {} of {}".format(word,
                      type(word)))
        raise TypeError("Invalid arg for param 'word': {} of {}".format(word,
                        type(word)))

    if not isinstance(word_list, (tuple, list)):
        logging.error("Invalid arg for param 'word_list': {} of {}".format(
                      word_list,
                      type(word_list)))
        raise TypeError("Invalid arg for param 'word_list': {} of {}".format(
                        word_list,
                        type(word_list)))

    anagrams = []

    word_sorted = sorted(word.lower())

    for word_to_compare in word_list:
        if word_sorted == sorted(word_to_compare.lower()):
            anagrams.append(word_to_compare.lower())
    return anagrams