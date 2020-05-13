from collections import Counter
from string import ascii_lowercase

import numpy as np
from consts import (
    DIGRAM_FREQS_ENGLISH,
    ENGLISH_LETTERS_BY_FREQUENCY,
    STANDARD_ALPHABET_SIZE,
)


class SimpleSolver:
    """Solver for simple monoalphabetic substitution ciphers."""

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

        # The decryption key is a string of letters that determines how the ciphertext
        # is converted to plaintext. The key is equal in length to the English alphabet
        # and is assumed to be in frequency order. In other words, the first letter is
        # the letter in the ciphertext that should be translated to an "e", the second
        # which one should be converted to a "t", and so on. When generating plaintext
        # this key will be converted to an alphabetical one that matches the order of
        # English alphabet which is the common way to express decryption keys.
        self._decryption_key = self._get_initial_key(ciphertext)

        self._ciphertext = ciphertext.lower()

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

        # First, count the number of occurrences of each letter and save to the index
        # that corresponds to the letter pair, i.e. frequencies[0, 0] is for "aa" etc.
        for i in range(0, text_length - 1):
            a = ascii_lowercase.index(text[i])
            b = ascii_lowercase.index(text[i + 1])
            frequencies[a, b] += 1

        # Replace each entry with a percentage of the total text length, to get the same
        # format as the English digram frequencies.
        rows, columns = frequencies.shape
        for i in range(rows):
            for j in range(columns):
                # All digram frequencies are in percentages, so convert it here too.
                frequencies[i, j] = 100 * frequencies[i, j] / text_length

        return frequencies

    def _common_to_alphabetical_key(self, key):
        alphabetical_key = [""] * STANDARD_ALPHABET_SIZE

        for key_letter, english_letter in zip(key, ENGLISH_LETTERS_BY_FREQUENCY):
            index = ascii_lowercase.index(english_letter)
            alphabetical_key[index] = key_letter

        return "".join(alphabetical_key)

    def _get_plaintext(self, decryption_key):
        if len(set(decryption_key)) != STANDARD_ALPHABET_SIZE:
            raise ValueError(f"Key must include all letters of the alphabet.")

        translation_table = {}

        for cipher_letter, plain_letter in zip(decryption_key, ascii_lowercase):
            translation_table[cipher_letter] = plain_letter

        return "".join([translation_table[c] for c in self._ciphertext])

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
        # We need this as a list so we can modify it in-place.
        key = [c for c in self._decryption_key]


        # Generate digram frequencies from the corresponding plaintext.
        putative_plaintext = self._get_plaintext(self._common_to_alphabetical_key(key))
        digram_frequencies = self._get_digram_frequencies(putative_plaintext)

        # Calculate initial score.
        best_score = self._score(digram_frequencies)

        # Loop and swap rows/columns in digram frequency matrix.
        for i in range(1, STANDARD_ALPHABET_SIZE):
            for j in range(STANDARD_ALPHABET_SIZE - i):
                # Try a potential swap in the digram frequency matrix.
                d = np.copy(digram_frequencies)
                self._swap(d, j, j + i)

                score = self._score(d)

                if score < best_score:
                    # The score improved, so commit this change in both the digram
                    # frequency matrix and the key.
                    digram_frequencies = d
                    key[j], key[j + i] = key[j + i], key[j]
                    best_score = score

        self._decryption_key = "".join(key)

    def plaintext(self):
        alphabetical_key = self._common_to_alphabetical_key(self._decryption_key)

        return self._get_plaintext(alphabetical_key)

    def reset(self):
        self._decryption_key = self._get_initial_key(self._ciphertext)
