import unittest
from string import ascii_lowercase

import numpy as np
from consts import (
    DIGRAM_FREQS_ENGLISH,
    ENGLISH_LETTER_FREQUENCIES,
    ENGLISH_LETTERS_BY_FREQUENCY,
    STANDARD_ALPHABET_SIZE,
)
from simple import SimpleSolver
from utils import alphabetical_to_common_key, common_to_alphabetical_key


class SimpleSolverTestCase(unittest.TestCase):
    def test_constants(self):
        self.assertTrue(100 - DIGRAM_FREQS_ENGLISH.sum() < 0.01)
        self.assertTrue(1 - sum(ENGLISH_LETTER_FREQUENCIES.values()) < 0.001)
        self.assertEqual(len(ENGLISH_LETTER_FREQUENCIES), STANDARD_ALPHABET_SIZE)
        self.assertEqual(len(ENGLISH_LETTERS_BY_FREQUENCY), STANDARD_ALPHABET_SIZE)

    def test_utils(self):
        items = (
            (ENGLISH_LETTERS_BY_FREQUENCY, ascii_lowercase),
            ("ocewzklnsxbfaqvthrdupmgijy", "eufbovhszimxqkwtjnlcaprgdy"),
        )

        # Test conversion from common to alphabetical key.
        for common_key, alpha_key in items:
            self.assertEqual(alpha_key, common_to_alphabetical_key(common_key))

        # Test conversion from alphabetical key to common key.
        for common_key, alpha_key in items:
            self.assertEqual(common_key, alphabetical_to_common_key(alpha_key))

    def test_get_initial_key(self):
        items = (
            ("aaabbc", "abcdefghijklmnopqrstuvwxyz"),
            ("aabbcc", "abcdefghijklmnopqrstuvwxyz"),
            ("abbccc", "cbadefghijklmnopqrstuvwxyz"),
            (ascii_lowercase, "abcdefghijklmnopqrstuvwxyz"),
            ("oegefotneeahtvawwlgtnecahtwe", "etawognhfvlcbdijkmpqrsuxyz"),
        )

        for ciphertext, expected_initial_key in items:
            s = SimpleSolver(ciphertext)
            self.assertEqual(s._get_initial_key(ciphertext), expected_initial_key)

    def test_get_plaintext(self):
        items = (
            (
                "qemeiqtxeeuktyuggjmtxesuktge",  # Ciphertext
                "etujdikzxgqswbmcfyhanpvlor",  # Common decryption key
                "defendtheeastwallofthecastle",  # Plaintext
            ),
            (
                "uaqaxuryaaljrklvvpqryadljrva",
                "arlpsxjcyvudgoqfekiwmntzbh",
                "defendtheeastwallofthecastle",
            ),
            (
                "dzyzedrjzzturbtsslyrjzntursz",
                "zrtlxeuqjsdnkpymgbhiacfwov",
                "defendtheeastwallofthecastle",
            ),
        )

        for ciphertext, common_key, expected_plaintext in items:
            s = SimpleSolver(ciphertext)
            self.assertEqual(s._get_plaintext(common_key), expected_plaintext)

    def test_swap(self):
        s = SimpleSolver("foo")

        # fmt: off
        items = (
            (np.array([
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9],
            ]), np.array([
                [5, 4, 6],
                [2, 1, 3],
                [8, 7, 9],
            ]), 0, 1),
            (np.array([
                [1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12],
                [13, 14, 15, 16],
            ]), np.array([
                [1, 4, 3, 2],
                [13, 16, 15, 14],
                [9, 12, 11, 10],
                [5, 8, 7, 6],
            ]), 1, 3),
        )
        # fmt: on

        for matrix, swapped, index1, index2 in items:
            s._swap(matrix, index1, index2)
            self.assertTrue(np.array_equal(matrix, swapped))

        # fmt: off
        items = (
            np.array([
                [1, 2],
                [4, 5],
                [7, 8],
            ]),
            np.array([
                [1, 2, 3],
                [4, 5, 6],
            ])
        )
        # fmt: on

        for matrix in items:
            with self.assertRaises(ValueError):
                s._swap(matrix, 0, 2)

    def test_get_digram_frequencies(self):
        s = SimpleSolver("foo")

        text = "abababaccz"

        digram_frequencies = s._get_digram_frequencies(text)

        # fmt: off
        expected_frequencies = np.array([
            [0, 30, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
        ])
        # fmt: on

        rows, columns = digram_frequencies.shape
        for i in range(rows):
            for j in range(columns):
                self.assertTrue(np.allclose(digram_frequencies, expected_frequencies))

    def test_score(self):
        s = SimpleSolver("foo")

        # If the score matrix is identical to English we have a "perfect" zero score.
        self.assertEqual(s._score(DIGRAM_FREQS_ENGLISH, DIGRAM_FREQS_ENGLISH), 0.0)

        # Scoring a zero matrix is the equivalent of scoring the English matrix.
        zero_array = np.zeros((STANDARD_ALPHABET_SIZE, STANDARD_ALPHABET_SIZE))
        self.assertEqual(s._score(zero_array), DIGRAM_FREQS_ENGLISH.sum())

        one_array = np.ones((STANDARD_ALPHABET_SIZE, STANDARD_ALPHABET_SIZE))
        self.assertTrue(abs(602.13 - s._score(one_array)) < 0.1)

        # fmt: off
        m1 = np.array([
            [1, 2],
            [3, 4],
        ])
        m2 = np.array([
            [2, 3],
            [4, 5],
        ])
        # fmt: on
        self.assertEqual(s._score(m1, m2), 4)

    def test_get_common_letters(self):
        s = SimpleSolver("foo")

        items = (
            ("aaabbc", "abc"),
            ("cccccbbbaaaad", "cabd"),
            ("aaaaaaaaaaaaaaaa", "a"),
        )

        for ciphertext, common_letters in items:
            self.assertEqual(common_letters, s._get_common_letters(ciphertext))

    def test_common_to_alphabetical_key(self):
        s = SimpleSolver("foo")

        items = (
            (ENGLISH_LETTERS_BY_FREQUENCY, ascii_lowercase),
            ("ocewzklnsxbfaqvthrdupmgijy", "eufbovhszimxqkwtjnlcaprgdy"),
        )

        for common_key, alpha_key in items:
            self.assertEqual(alpha_key, s._common_to_alphabetical_key(common_key))
