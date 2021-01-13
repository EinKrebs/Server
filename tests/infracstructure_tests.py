import unittest
import random


class IteratorExtensionsTests(unittest.TestCase):
    def test_to_dictionary_random(self):
        random.seed(100)
        keys = set(random.randint(1, 100000) for _ in range(10000))
        pairs = list((key, random.randint(1, 1000000)) for key in keys)
        dictionary = dict(pairs)
        try:
            for key, value in pairs:
                self.assertEqual(dictionary[key], value)
        except KeyError:
            self.fail("Missing key")
