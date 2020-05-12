from string import ascii_lowercase

import numpy as np
from consts import STANDARD_ALPHABET_SIZE
from solver import AbstractSolver


class SimpleSolver(AbstractSolver):
    """Solver for simple monoalphabetic and polyalphabetic substitution ciphers."""

    def __init__(self, ciphertext):
        # The decryption key is a string of letters that determines how the ciphertext
        # is converted to plaintext. The key is equal in length to the English alphabet
        # and is assumed to be in frequency order. In other words, the first letter is
        # the letter in the ciphertext that should be translated to an "e", the second
        # which one should be converted to a "t", and so on.
        self._decryption_key = self._get_initial_key(ciphertext)

        super().__init__(ciphertext)

    def _get_initial_key(self, ciphertext):
        """Construct the initial decryption key.

        The initial decryption key is based on the letter frequencies in the ciphertext,
        meaning an assumption that the most common letter in the ciphertext translates
        to the most common letter in the English language, and so on. Any letters not
        present in the ciphertext will be added alphabetically at the end of the key.

        Parameters
        ----------
        ciphertext : str
            The ciphertext to generate an initial decryption key from.

        Returns
        -------
        decryption_key : str
            The initial decryption key.
        """

        decryption_key = self._get_common_letters(ciphertext)

        for c in ascii_lowercase:
            if c not in decryption_key:
                decryption_key += c

        return "".join(decryption_key)

    def _swap(self, matrix, index1, index2):
        """Swap the matrix rows and columns at the given indices."""

        rows, columns = matrix.shape

        if rows != columns:
            raise ValueError("Matrix must be square.")

        # Swap rows:
        matrix[[index1, index2]] = matrix[[index2, index1]]

        # Swap columns:
        matrix[:, [index1, index2]] = matrix[:, [index2, index1]]

    def solve(self):
        key = [c for c in self._decryption_key]

        print(f"starting with key = {key}")

        # Generate digram frequencies from the corresponding plaintext.
        putative_plaintext = self._get_plaintext(key)
        digram_frequencies = self._get_digram_frequencies(putative_plaintext)

        # Calculate initial score.
        best_score = self._score(digram_frequencies)
        print(f"best_score = {best_score}")

        # Loop and swap rows/columns in digram frequency matrix.
        for i in range(1, STANDARD_ALPHABET_SIZE):
            for j in range(STANDARD_ALPHABET_SIZE - i):
                # Try a potential swap in the digram frequency matrix.
                d = np.copy(digram_frequencies)
                # print(f"Swapping index {j} and {j + i}")
                self._swap(d, j, j + i)

                # See if the new matrix has a better score.
                score = self._score(d)
                print(f"score = {score}")

                if score < best_score:
                    print(f"new best_score = {score}")
                    # The score improved, so commit this change in both the digram
                    # frequency matrix and the key.
                    digram_frequencies = d
                    key[j], key[j + i] = key[j + i], key[j]
                    best_score = score

        self._decryption_key = "".join(key)
        print(f"final key: {self._decryption_key}")

    def plaintext(self):
        return self._get_plaintext(self._decryption_key)

    def reset(self):
        self._decryption_key = self._get_initial_key(self._ciphertext)
