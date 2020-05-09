import unittest
from string import ascii_lowercase

from consts import DIGRAM_FREQS_ENGLISH, STANDARD_ALPHABET_LENGTH
from homophonic import HomophonicSolver


class ConstTestCase(unittest.TestCase):
    """Tests to verify the integrity of all constants."""

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


class DigramFrequenciesTestCase(unittest.TestCase):
    """Test to verify all digram frequency generation methods."""

    def test_get_digram_frequencies(self):
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
