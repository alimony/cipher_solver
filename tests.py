import unittest
from string import ascii_lowercase

import numpy as np
from consts import DIGRAM_FREQS_ENGLISH, STANDARD_ALPHABET_LENGTH
from homophonic import HomophonicSolver


class HomophonicSolverTestCase(unittest.TestCase):
    """Test suite for the homophonic solver."""

    def test_solver_init(self):
        """Test basic initialisation of solver."""

        with self.assertRaises(TypeError):
            HomophonicSolver()
        with self.assertRaises(ValueError):
            HomophonicSolver(123)
        with self.assertRaises(ValueError):
            HomophonicSolver([])
        with self.assertRaises(ValueError):
            HomophonicSolver("")

        HomophonicSolver("abcdef")

    def test_english_digram_frequencies(self):
        """Test a few samples from the digram source at http://norvig.com/mayzner.html
        to make sure the values have the correct positions in our array."""

        def _get_freq(digram):
            a, b = digram
            row = ascii_lowercase.index(a)
            col = ascii_lowercase.index(b)

            return DIGRAM_FREQS_ENGLISH[row][col]

        # These should pass.
        digrams = (
            ("ri", 0.00728),
            ("in", 2.00433),
            ("wt", 0.00007),
            ("ew", 0.00117),
            ("se", 0.00932),
        )

        for digram, freq in digrams:
            self.assertEqual(_get_freq(digram), freq)

        # These should fail.
        digrams = (
            ("cc", 0.00728),
            ("km", 2.00433),
            ("au", 0.00007),
            ("zi", 0.00117),
            ("rp", 0.00932),
        )

        for digram, freq in digrams:
            self.assertNotEqual(_get_freq(digram), freq)

    def test_get_digram_frequencies(self):
        """Test generation of digram frequency matrices."""

        def _unique_digrams(frequencies):
            rows, columns = frequencies.shape
            num_nonzero = 0
            for i in range(rows):
                for j in range(columns):
                    value = frequencies[i, j]
                    if value > 0:
                        num_nonzero += 1
            return num_nonzero

        h = HomophonicSolver("foo")

        text = "abcdefghijk"
        frequencies = h._get_digram_frequencies(text, standard_size=True)

        self.assertEqual(
            frequencies.shape, (STANDARD_ALPHABET_LENGTH, STANDARD_ALPHABET_LENGTH)
        )

        # The frequencies array should now have mostly zeros, but one non-zero entry for
        # each unique digram in the text. In this case all digrams are unique.
        self.assertEqual(_unique_digrams(frequencies), len(text) - 1)

        text = "abcabcdefghiijjkk"
        frequencies = h._get_digram_frequencies(text, standard_size=True)
        self.assertEqual(_unique_digrams(frequencies), 14)

        # Check some specific array elements.
        self.assertTrue(
            frequencies[2, 0] - (1 / 626) < 0.0000000  # Digram "ca" occurs one time.
        )
        self.assertTrue(
            frequencies[2, 0] - (2 / 626) < 0.0000000  # Digram "ab" occurs two times.
        )
        self.assertEqual(
            frequencies[25, 25], 0.0000000  # Digram "zz" occurs zero times.
        )

    def test_score(self):
        """Test the scoring function for digram frequency matrices."""

        h = HomophonicSolver("foo")

        a = np.array([[1, 2], [3, 4]])
        b = np.array([[5, 6], [7, 8]])

        self.assertEqual(h._score(a, b), 16)

        with self.assertRaises(ValueError):
            h._score(a)

        c = np.ones((STANDARD_ALPHABET_LENGTH, STANDARD_ALPHABET_LENGTH))

        self.assertEqual(h._score(c), 658.43119)

    def test_get_num_distinct_letters(self):
        """Test getting the number of distinct letters in a text."""

        h = HomophonicSolver("foo")

        items = (
            ("", 0),
            ("a", 1),
            ("ab", 2),
            ("aabb", 2),
            ("aaabbbccc", 3),
            ("aaabbc", 3),
        )

        for text, num_letters in items:
            self.assertEqual(h._get_num_distinct_letters(text), num_letters)
