from collections import Counter
from random import randint
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

    def _get_plaintext(self, decryption_key):
        if len(set(decryption_key)) != STANDARD_ALPHABET_SIZE:
            raise ValueError(f"Key must include all letters of the alphabet.")

        # The decryption key will be in order of most common first, so we need to
        # construct a list of indices where to insert each to get an "alphabetical key"
        # instead.
        indices = [ascii_lowercase.index(letter) for letter in ascii_lowercase]

        translation_table = {}

        for cipher_letter, index in zip(decryption_key, indices):
            plain_letter = ascii_lowercase[index]
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

    def _solve_naive(self):
        # We need this as a list so we can modify it in-place.
        key = [c for c in self._decryption_key]

        putative_plaintext = self._get_plaintext(key)
        digram_frequencies = self._get_digram_frequencies(putative_plaintext)

        best_score = self._score(digram_frequencies)

        iterations_since_last_improvement = 0

        while iterations_since_last_improvement < 1000:
            k = key[:]
            a = randint(0, 25)
            b = randint(0, 25)
            k[a], k[b] = k[b], k[a]
            p = self._get_plaintext(k)
            d = self._get_digram_frequencies(p)
            score = self._score(d)
            iterations_since_last_improvement += 1
            if score < best_score:
                best_score = score
                key = k[:]
                iterations_since_last_improvement = 0

        self._decryption_key = "".join(key)

    def _solve_fast(self):
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

    def solve(self):
        self._solve_naive()

    def plaintext(self):
        return self._get_plaintext(self._decryption_key)

    def reset(self):
        self._decryption_key = self._get_initial_key(self._ciphertext)
