from abc import ABC, abstractmethod
from collections import Counter
from string import ascii_lowercase

import numpy as np
from consts import (
    DIGRAM_FREQS_ENGLISH,
    ENGLISH_LETTERS_BY_FREQUENCY,
    STANDARD_ALPHABET_SIZE,
)


class AbstractSolver(ABC):
    def __init__(self, ciphertext):
        """Create new solver.

        This creates a new cipher solver from an initial ciphertext.

        Parameters
        ----------
        ciphertext : str
            The ciphertext to solve.

        Raises
        ------
        ValueError
            If the passed ciphertext is not a string, or is empty.
        """

        if not isinstance(ciphertext, str):
            raise ValueError(f"{ciphertext} is not a string.")

        if len(ciphertext) < 1:
            raise ValueError("Ciphertext cannot be empty.")

        self._ciphertext = ciphertext.lower()

        super().__init__()

    def _score(self, matrix1, matrix2=DIGRAM_FREQS_ENGLISH):
        if matrix1.shape != matrix2.shape:
            raise ValueError("Digram frequency matrices must have the same dimensions")

        return abs(matrix1 - matrix2).sum()

    def _get_common_letters(self, text):
        c = Counter(text)
        return "".join([letter[0] for letter in c.most_common()])

    def _get_digram_frequencies(self, text, alphabet_size=STANDARD_ALPHABET_SIZE):
        """Generate digram frequencies for the passed text.

        Parameters
        ----------
        text : str
            Text to generate digram frequencies for.

        Returns
        -------
        digram_frequencies : numpy.array
            An array of digram frequencies indexed by [first][second] letter.
        """

        frequencies = np.zeros((alphabet_size, alphabet_size))

        text = text.lower()
        text_length = len(text)

        for i in range(0, text_length - 1):
            a = ascii_lowercase.index(text[i])
            b = ascii_lowercase.index(text[i + 1])
            frequencies[a, b] += 1

        # Replace each entry with a percentage of the total text length, to get the same
        # format as the English digram frequencies.
        rows, columns = frequencies.shape
        for i in range(rows):
            for j in range(columns):
                frequencies[i, j] = 100 * frequencies[i, j] / text_length

        return frequencies

    def _get_plaintext(self, decryption_key):
        if len(set(decryption_key)) != STANDARD_ALPHABET_SIZE:
            raise ValueError(f"Key must include all letters of the alphabet.")

        translation_table = {}

        for cipher_letter, plain_letter in zip(decryption_key, ascii_lowercase):
            translation_table[cipher_letter] = plain_letter

        return "".join([translation_table[c] for c in self._ciphertext])

    @abstractmethod
    def solve(self):
        """Run the solver."""

        pass

    @abstractmethod
    def plaintext(self):
        """Return the current plaintext solution.

        Returns
        -------
        plaintext : str or None
            The current plaintext solution, or None of solver hasn't run.
        """

        pass

    @abstractmethod
    def reset(self):
        """Discard the current solution and reset the solver."""

        pass
