import unittest
from string import ascii_lowercase

from consts import DIGRAM_FREQS_ENGLISH


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
