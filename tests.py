import unittest
from string import ascii_uppercase

from consts import DIGRAM_FREQS_ENGLISH


class ConstTestCase(unittest.TestCase):
    """Tests to verify the integrity of all constants."""

    def test_english_digram_frequencies(self):
        """Test a few samples from the digram source at http://norvig.com/mayzner.html
        to make sure the values have the correct positions in our array."""

        def _get_freq(digram):
            a, b = digram
            row = ascii_uppercase.index(a)
            col = ascii_uppercase.index(b)

            return DIGRAM_FREQS_ENGLISH[row][col]

        # These should pass.
        digrams = (
            ("RI", 0.00728),
            ("IN", 2.00433),
            ("WT", 0.00007),
            ("EW", 0.00117),
            ("SE", 0.00932),
        )

        for digram, freq in digrams:
            self.assertEqual(_get_freq(digram), freq)

        # These should fail.
        digrams = (
            ("CC", 0.00728),
            ("KM", 2.00433),
            ("AU", 0.00007),
            ("ZI", 0.00117),
            ("RP", 0.00932),
        )

        for digram, freq in digrams:
            self.assertNotEqual(_get_freq(digram), freq)
