import unittest
from string import ascii_lowercase

import numpy as np
from consts import DIGRAM_FREQS_ENGLISH, STANDARD_ALPHABET_SIZE
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
            frequencies.shape, (STANDARD_ALPHABET_SIZE, STANDARD_ALPHABET_SIZE)
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

        c = np.ones((STANDARD_ALPHABET_SIZE, STANDARD_ALPHABET_SIZE))

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

    def test_get_frequency_distribution(self):
        """Test calculation of frequency distributions."""

        h = HomophonicSolver("foo")

        # fmt: off
        items = (
            (26, np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])),  # noqa
            (27, np.array([1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])),  # noqa
            (35, np.array([2, 1, 1, 1, 3, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1])),  # noqa
            (45, np.array([3, 1, 1, 1, 5, 1, 1, 2, 3, 1, 1, 1, 1, 3, 3, 1, 1, 2, 3, 4, 1, 1, 1, 1, 1, 1])),  # noqa
            (55, np.array([4, 1, 1, 2, 7, 1, 1, 2, 4, 1, 1, 2, 1, 4, 4, 1, 1, 3, 3, 5, 1, 1, 1, 1, 1, 1])),  # noqa
            (65, np.array([5, 1, 2, 2, 8, 1, 1, 3, 5, 1, 1, 2, 1, 5, 5, 1, 1, 4, 4, 6, 1, 1, 1, 1, 1, 1])),  # noqa
            (75, np.array([6, 1, 2, 3, 9, 1, 1, 4, 6, 1, 1, 3, 1, 5, 6, 1, 1, 4, 5, 7, 2, 1, 1, 1, 1, 1])),  # noqa
            (85, np.array([7, 1, 3, 3,11, 2, 1, 4, 6, 1, 1, 3, 2, 6, 7,1, 1, 5, 5, 8, 2, 1, 1, 1, 1, 1])),  # noqa
            (95, np.array([8, 1, 3, 3, 12, 2, 1, 5, 7, 1, 1, 4, 2, 7, 7, 2, 1, 6, 6, 9, 2, 1, 1, 1, 1, 1])),  # noqa
        )
        # fmt: on

        for alphabet_size, distribution in items:
            self.assertTrue(
                np.array_equal(
                    h._get_frequency_distribution(alphabet_size), distribution
                )
            )
