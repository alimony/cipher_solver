import random
import unittest
from string import ascii_lowercase

import numpy as np
from consts import (
    DIGRAM_MATRIX_ENGLISH,
    ENGLISH_LETTER_FREQUENCIES,
    ENGLISH_LETTERS_BY_FREQUENCY,
    STANDARD_ALPHABET_SIZE,
)
from simple import SimpleSolver
from utils import alphabetical_to_common_key, common_to_alphabetical_key, encrypt


class SimpleSolverTestCase(unittest.TestCase):
    def test_constants(self):
        self.assertTrue(100 - DIGRAM_MATRIX_ENGLISH.sum() < 0.01)
        self.assertTrue(1 - sum(ENGLISH_LETTER_FREQUENCIES.values()) < 0.001)
        self.assertEqual(len(ENGLISH_LETTER_FREQUENCIES), STANDARD_ALPHABET_SIZE)
        self.assertEqual(len(ENGLISH_LETTERS_BY_FREQUENCY), STANDARD_ALPHABET_SIZE)

    def test_utils(self):
        items = (
            (ENGLISH_LETTERS_BY_FREQUENCY, ascii_lowercase),
            ("ocewzklnsxbfaqvthrdupmgijy", "eufbovhszimxqkwtjnlcaprgdy"),
        )

        # Test conversion from common to alphabetical key.
        for common_key, alphabetical_key in items:
            self.assertEqual(alphabetical_key, common_to_alphabetical_key(common_key))

        # Test conversion from alphabetical key to common key.
        for common_key, alphabetical_key in items:
            self.assertEqual(common_key, alphabetical_to_common_key(alphabetical_key))

        # Test encrypting from ciphertext and alphabetical key.
        items = (
            (
                "I am already far north of London.",
                "jhdxmuvpltbwnayzscrefqogik",
                "L jn jwcmjxi ujc aycep yu Wyaxya.",
            ),
            (
                "I am already far north of London.",
                ascii_lowercase,
                "I am already far north of London.",
            ),
        )

        for plaintext, alphabetical_key, ciphertext in items:
            self.assertEqual(encrypt(plaintext, alphabetical_key), ciphertext)

    def test_init(self):
        s = SimpleSolver("foo")

        self.assertEqual(s._decryption_key, list("ofabcdeghijklmnpqrstuvwxyz"))
        self.assertEqual(s._ciphertext, "foo")

        items = ("", [], None)

        for arg in items:
            with self.assertRaises(ValueError):
                s = SimpleSolver(arg)

    def test_get_initial_key(self):
        items = (
            ("aaabbc", list("abcdefghijklmnopqrstuvwxyz")),
            ("aabbcc", list("abcdefghijklmnopqrstuvwxyz")),
            ("abbccc", list("cbadefghijklmnopqrstuvwxyz")),
            (ascii_lowercase, list("abcdefghijklmnopqrstuvwxyz")),
            ("oegefotneeahtvawwlgtnecahtwe", list("etawognhfvlcbdijkmpqrsuxyz")),
        )

        for ciphertext, expected_initial_key in items:
            s = SimpleSolver(ciphertext)
            self.assertEqual(s._get_initial_key(ciphertext), expected_initial_key)

        items = ("", [], None)

        for ciphertext in items:
            with self.assertRaises(ValueError):
                s._get_initial_key(ciphertext)

    def test_get_common_letters(self):
        s = SimpleSolver("foo")

        items = (
            ("aaabbc", list("abc")),
            ("cccccbbbaaaad", list("cabd")),
            ("aaaaaaaaaaaaaaaa", ["a"]),
        )

        for ciphertext, common_letters in items:
            self.assertEqual(common_letters, s._get_common_letters(ciphertext))

        items = ("", [], None)

        for ciphertext in items:
            with self.assertRaises(ValueError):
                s._get_common_letters(ciphertext)

    def test_get_digram_matrix(self):
        s = SimpleSolver("foo")

        # fmt: off
        expected_frequencies = np.array([
            # e, t, a, o, ...
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 30, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # noqa
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],  # noqa
        ])
        # fmt: on

        # These should all yield the same digram matrix since case and special chars are
        # ignored when calculating it.
        items = (
            "abababacczz",
            "aBabAbacCzz",
            "ABABABACCZz",
            "*zz**ABab ..abac ba ...cc-cZ",
        )

        for text in items:
            digram_frequencies = s._get_digram_matrix(text)
            rows, columns = digram_frequencies.shape
            self.assertTrue(np.allclose(digram_frequencies, expected_frequencies))

        items = ("a", "", [], None)

        for text in items:
            with self.assertRaises(ValueError):
                s._get_digram_matrix(text)

    def test_score(self):
        s = SimpleSolver("foo")

        # If the score matrix is identical to English we have a "perfect" zero score.
        self.assertEqual(s._score(DIGRAM_MATRIX_ENGLISH, DIGRAM_MATRIX_ENGLISH), 0.0)

        # Scoring a zero matrix is the equivalent of scoring the English matrix.
        zero_array = np.zeros((STANDARD_ALPHABET_SIZE, STANDARD_ALPHABET_SIZE))
        self.assertEqual(s._score(zero_array), DIGRAM_MATRIX_ENGLISH.sum())

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

        with self.assertRaises(ValueError):
            s._score(np.array([1, 2]), np.array([1, 2, 3]))

    def test_swap_matrix(self):
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
            s._swap_matrix(matrix, index1, index2)
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
                s._swap_matrix(matrix, 0, 2)

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
            # Make sure case and special chars are preserved:
            (
                "Lorem ipsum dolor sit amet, consectetur adipisicing elit.",
                ENGLISH_LETTERS_BY_FREQUENCY,
                "Lorem ipsum dolor sit amet, consectetur adipisicing elit.",
            ),
        )

        for ciphertext, common_key, expected_plaintext in items:
            s = SimpleSolver(ciphertext)
            self.assertEqual(s._get_plaintext(common_key), expected_plaintext)

        with self.assertRaises(ValueError):
            s._get_plaintext("abc")

        with self.assertRaises(ValueError):
            s._get_plaintext(ascii_lowercase[1:])

    def test_public_api(self):
        s = SimpleSolver("qemeiqtxeeuktyuggjmtxesuktge")

        self.assertEqual(s.plaintext(), "ienehitseeartlaoodntsecartoe")

        k = s._decryption_key

        # After solving, the decryption key should have changed.
        s.solve()
        self.assertNotEqual(k, s._decryption_key)

        # After resetting, the decryption key should be back to the default one.
        s.reset()
        self.assertEqual(k, s._decryption_key)

        # Should return the decryption key in alphabetical form.
        self.assertEqual(s.decryption_key(), "unsjecfiqvpybmgdwkxtaohrlz")

        # Method doesn't exist.
        with self.assertRaises(ValueError):
            s.solve(method="foo")

        # Use the original key swap method.
        s.solve(method="deterministic")

    def test_matrix_key_swap(self):
        # The algorithm is based on the premise that if a digram matrix is created from
        # a plaintext using a certain key, swapping the letters at index (a, b) in that
        # key and creating a new plaintext using the modified key, the digram matrix for
        # that new plaintext will be identical to the first matrix but with the rows and
        # columns at index (a, b) swapped. In other words, swapping rows and columns in
        # the digram matrix is equivalent to swapping letters in the key. We need to
        # test that this premise holds.

        # We might as well test that this is true for all possible swaps.
        for a in range(STANDARD_ALPHABET_SIZE):
            for b in range(STANDARD_ALPHABET_SIZE):
                if a == b:
                    continue

                ciphertext = "".join(random.choices(ascii_lowercase, k=100))

                s = SimpleSolver(ciphertext)

                plaintext1 = s.plaintext()
                matrix1 = s._get_digram_matrix(plaintext1)

                # First, swap rows and columns in the original matrix.
                s._swap_matrix(matrix1, a, b)

                # Then make the same swap in the key and generate a new matrix.
                key = [c for c in s._decryption_key]
                key[a], key[b] = key[b], key[a]
                s._decryption_key = "".join(key)
                plaintext2 = s.plaintext()
                matrix2 = s._get_digram_matrix(plaintext2)

                # We now have the original matrix where we swapped rows and columns,
                # and the new matrix that was generated from plaintext using the key
                # in which we swapped the letters at the same index.
                self.assertTrue(np.allclose(matrix1, matrix2))
