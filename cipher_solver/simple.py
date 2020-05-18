import random
from collections import Counter
from string import ascii_lowercase, ascii_uppercase

import numpy as np
from cipher_solver.consts import (
    DIGRAM_MATRIX_ENGLISH,
    ENGLISH_LETTERS_BY_FREQUENCY,
    RANDOM_INDEX_DISTRIBUTION,
    STANDARD_ALPHABET_SIZE,
)
from cipher_solver.utils import common_to_alphabetical_key


class SimpleSolver:
    """Solver for simple monoalphabetic substitution ciphers.

    This solver is based on the paper
    "A Fast Method for the Cryptanalysis of Substitution Ciphers" by Thomas Jakobsen.
    The details of the algorithm is described in the solve method docstrings.

    The following terminology is used:

    "ciphertext" : The encrypted text we want to solve to get a plaintext.
    "plaintext" : The decrypted plaintext using a certain decryption key.
    "common key" : Key used to generate a plaintext, ordered by most common letter.
    "alphabetical key" : Decryption key, but ordered alphabetically.
    "decryption key" : Assumed to mean a common key if nothing else is specified.
    "digram" : A pair of letters, e.g. "aa", "cd" etc.
    "digram matrix" : An (n x n) matrix, where n is the length of the used alphabet,
                      created from a given text, where the frequency of each digram
                      relative to the text length is saved to the corresponding index
                      pair, e.g. (0, 0) for "aa", (0, 1) for "ab" etc.
    "distance sum" : The method used to score solutions, see ._score() for details.
    """

    def __init__(self, ciphertext):
        """Create new solver.

        Creates a new cipher solver from an initial ciphertext.

        Parameters
        ----------
        ciphertext : str
            The ciphertext to solve.

        Raises
        ------
        ValueError
            If the passed ciphertext is not a string.
            If the passed ciphertext is empty.
        """

        if not isinstance(ciphertext, str):
            raise ValueError(f"{ciphertext} is not a string.")

        if len(ciphertext) < 1:
            raise ValueError("Ciphertext cannot be empty.")

        # The decryption key is a list of letters that determines how the ciphertext is
        # converted to plaintext. The key is equal in length to the English alphabet and
        # is assumed to be in frequency order. In other words, the first letter is the
        # letter in the ciphertext that should be translated to an "e", the second
        # which one should be converted to a "t", and so on.
        self._decryption_key = self._get_initial_key(ciphertext)

        self._ciphertext = ciphertext

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
        decryption_key : list
            The initial decryption key.

        Raises
        ------
        ValueError
            If the passed ciphertext is not a string.
            If the passed ciphertext is empty.
        """

        if not isinstance(ciphertext, str):
            raise ValueError(f"{ciphertext} is not a string.")

        if len(ciphertext) < 1:
            raise ValueError("Ciphertext cannot be empty.")

        decryption_key = self._get_common_letters(ciphertext)

        for c in ascii_lowercase:
            if c not in decryption_key:
                decryption_key += c

        return decryption_key

    def _get_common_letters(self, text):
        """Get all unique letters of the passed text, sorted by frequency.

        Parameters
        ----------
        text : str
            The text to find most common letters for.

        Returns
        -------
        common_letters : list
            The letters of the text ordered by frequency.

        Raises
        ------
            If the passed text is not a string.
            If the passed text is empty.
        """

        if not isinstance(text, str):
            raise ValueError("{text} is not a string.")

        if len(text) < 1:
            raise ValueError("Text must not be empty.")

        c = Counter(text)
        return [letter[0] for letter in c.most_common() if letter[0] in ascii_lowercase]

    def _get_digram_matrix(self, text):
        """Generate digram matrix for the passed text.

        Parameters
        ----------
        text : str
            Text to generate digram frequency matrix for.

        Returns
        -------
        digram_matrix : numpy.array
            An array of digram frequencies indexed by [first][second] letter.

        Raises
        ------
        ValueError
            If the passed text is not a string.
            If the passed text does not contain at least one digram.
        """

        if not isinstance(text, str):
            raise ValueError(f"{text} is not a string.")

        if len(text) < 2:
            raise ValueError("Text must contain at least one digram.")

        digram_matrix = np.zeros((STANDARD_ALPHABET_SIZE, STANDARD_ALPHABET_SIZE))

        text = text.lower()
        text_length = len(text)

        # First, count the number of occurrences of each letter and save to the index
        # that corresponds to the letter pair based on where it is in the English
        # alphabet in frequency order.
        num_digrams = 0
        for i in range(0, text_length - 1):
            char1 = text[i]
            char2 = text[i + 1]

            # Only count true digrams, i.e. where both chars are actual letters.
            if char1 not in ascii_lowercase or char2 not in ascii_lowercase:
                continue

            a = ENGLISH_LETTERS_BY_FREQUENCY.index(char1)
            b = ENGLISH_LETTERS_BY_FREQUENCY.index(char2)

            digram_matrix[a, b] += 1
            num_digrams += 1

        # Replace each entry with a percentage of the total number of digrams, to get
        # the same format as the English digram matrix.
        rows, columns = digram_matrix.shape
        for i in range(rows):
            for j in range(columns):
                # All digram frequencies are in percentages, so convert it here too.
                digram_matrix[i, j] = 100 * digram_matrix[i, j] / num_digrams

        return digram_matrix

    def _score(self, matrix1, matrix2=DIGRAM_MATRIX_ENGLISH):
        """Calculate a score for passed digram matrices using the distance sum method.

        The score is defined as the sum of all the absolute differences between each
        corresponding element in the two matrices.

        Parameters
        ----------
        matrix1 : numpy.array
            The first matrix to use in the comparison.
        matrix2 : numpy.array
            The second matrix to use in the comparison. Defaults to English digrams.

        Returns
        -------
        score : float
            The distance sum of the two matrices.

        Raises
        ------
        ValueError
            If the passed matrices don't have the same number of rows and columns.
        """

        if matrix1.shape != matrix2.shape:
            raise ValueError("Digram matrices must have the same dimensions")

        return abs(matrix1 - matrix2).sum()

    def _swap_matrix(self, matrix, index1, index2):
        """Swap the matrix rows and columns at the given indices.

        Parameters
        ----------
        matrix : numpy.array
            The matrix to modify in-place.
        index1 : int
            The first index to swap between.
        index2 : int
            The second index to swap between.

        Raises
        ------
        ValueError
            If the passed matrix is not square.
        """

        rows, columns = matrix.shape

        if rows != columns:
            raise ValueError("Matrix must be square.")

        # Swap rows:
        matrix[[index1, index2]] = matrix[[index2, index1]]

        # Swap columns:
        matrix[:, [index1, index2]] = matrix[:, [index2, index1]]

    def _get_plaintext(self, decryption_key):
        """Return a plaintext using the passed decryption key.

        Parameters
        ----------
        decryption_key : list
            The decryption key to use for generating the plaintext.

        Returns
        -------
        plaintext : str
            Plaintext from decrypting the ciphertext using the passed decryption key.

        Raises
        ------
        ValueError
            If the passed decryption key does not contain all letters of the alphabet.
        """

        if len(set(decryption_key)) != STANDARD_ALPHABET_SIZE:
            raise ValueError("Key must include all letters of the alphabet.")

        # The decryption key will be in order of most common first, so we need to
        # construct a list of indices where to insert each to get an alphabetical key.
        indices = [
            ascii_lowercase.index(letter) for letter in ENGLISH_LETTERS_BY_FREQUENCY
        ]

        translation_table = {}

        for key_letter, index in zip(decryption_key, indices):
            plain_letter = ascii_lowercase[index]
            translation_table[key_letter] = plain_letter

        plaintext = ""

        for c in self._ciphertext:
            is_upper = c in ascii_uppercase
            letter = translation_table.get(c.lower(), c)
            if is_upper:
                letter = letter.upper()
            plaintext += letter

        return plaintext

    def _weighted_random_index_pair(self):
        """Return a random index pair for swapping, weighted by letter frequency.

        Instead of just picking random indices between zero and the alphabet length,
        which will suggest very unlikely swaps, the indices are randomised with a weight
        according to English letter frequency. In other words, low indices
        (corresponding to common letters) will be suggested more often than high indices
        (corresponding to uncommon letters).

        Returns
        -------
        index_pair : list
            A pair of random indices between zero and the alphabet length.
        """

        return random.sample(RANDOM_INDEX_DISTRIBUTION, 2)

    def _solve_deterministic(self):
        """Solve the cipher using predefined, structured digram matrix swaps.

        This is the algorithm described by Jakobsen. It is based on the insight that
        swapping rows and columns in a digram matrix is equivalent to swapping the
        elements at the same indices in the key that was used to generate the plaintext
        that was used to generate the digram matrix.

        The algorithm works as follows:

        1. Create an initial key that is the ciphertext letters ordered by frequency.
        2. Generate a putative plaintext using this key.
        3. Generate a digram matrix from this plaintext.
        4. Calculate a score from this digram matrix using the distance sum method.
        5. Repeat the following steps:
            6a. Make a copy of the digram matrix.
            6b. Swap rows/elements of this putative digram matrix at index (0, 1),
                (1, 2), (2, 3) etc. until the last index of the pair reaches the
                alphabet length. Then swap rows/columns at index (0, 2), (1, 3), (2, 4)
                etc. until the last index in the pair reaches the alphabet length. The
                last swap in this nested loop will be (0, 25).
            6c. After each swap, calculate a score from the modified digram matrix.
            6d. If the score improved, save the modified digram matrix as the new best
                digram matrix, make the same swap in the key and save it as the new best
                key, and save the improved score as the new best score.
        7. The algorithm is done when all swaps have been made.
        """

        # We need this as a list so we can modify it in-place.
        key = self._decryption_key[:]

        # Generate digram matrix from the corresponding plaintext.
        putative_plaintext = self._get_plaintext(key)
        digram_matrix = self._get_digram_matrix(putative_plaintext)

        # Calculate initial score.
        best_score = self._score(digram_matrix)

        # Loop and swap rows/columns in digram matrix.
        for i in range(1, STANDARD_ALPHABET_SIZE):
            for j in range(STANDARD_ALPHABET_SIZE - i):
                # Try a potential swap in the digram matrix.
                d = np.copy(digram_matrix)
                self._swap_matrix(d, j, j + i)

                score = self._score(d)

                if score < best_score:
                    # The score improved, so commit this change in both the digram
                    # matrix and the key.
                    digram_matrix = np.copy(d)
                    key[j], key[j + i] = key[j + i], key[j]
                    best_score = score

        self._decryption_key = key[:]

    def _solve_random(self):
        """Solve the cipher using random key swaps.

        This is the algorithm described by Jakobsen, but using random key swaps instead
        of the original structured swaps according to a certain pattern.

        The algorithm works as follows:

        1. Create an initial key that is the ciphertext letters ordered by frequency.
        2. Generate a putative plaintext using this key.
        3. Generate a digram matrix from this plaintext.
        4. Calculate a score from this digram matrix using the distance sum method.
        5. Repeat the following steps:
            6a. Make a copy of the digram matrix.
            6b. Swap two rows/column at random in this putative digram matrix.
            6c. Calculate a score for the putative digram matrix.
            6d. If the score improved, save the putative digram matrix as the new best
                digram matrix, make the same swap in the key, and save the improved
                score as the new best score.
        7. The algorithm is done when the score hasn't improved for 2,000 iterations.
        """

        # We need the key as a list so we can modify it in-place.
        key = self._decryption_key[:]

        # Generate an initial digram matrix.
        putative_plaintext = self._get_plaintext(key)
        digram_matrix = self._get_digram_matrix(putative_plaintext)

        best_score = self._score(digram_matrix)

        iterations_since_last_improvement = 0

        # Loop and swap elements in the key at random until the score hasn't improved
        # for 1,000 iterations.
        while iterations_since_last_improvement < 2000:
            a, b = self._weighted_random_index_pair()

            putative_digram_matrix = np.copy(digram_matrix)
            self._swap_matrix(putative_digram_matrix, a, b)
            score = self._score(putative_digram_matrix)

            if score < best_score:
                best_score = score
                digram_matrix = np.copy(putative_digram_matrix)
                key[a], key[b] = key[b], key[a]
                iterations_since_last_improvement = 0
            else:
                iterations_since_last_improvement += 1

        self._decryption_key = key[:]

    def solve(self, method="random"):
        """Solve the cipher.

        Run the solver and save the resulting decryption key.

        Parameters
        ----------
        method : str
            The method to use when solving, currently "random" or "deterministic".

        Raises
        ------
        ValueError
            If the passed method is unknown.
        """

        if method == "random":
            self._solve_random()
        elif method == "deterministic":
            self._solve_deterministic()
        else:
            raise ValueError(f"Unknown method {method}")

    def plaintext(self):
        """Return a plaintext using the current decryption key.

        Returns
        -------
        plaintext : str
            Plaintext from decrypting the ciphertext using the current decryption key.
        """

        return self._get_plaintext(self._decryption_key)

    def decryption_key(self):
        """Return the current alphabetical decryption key.

        Returns
        -------
        alphabetical_key : str
            The current decryption key as a string in alphabetical form.
        """

        return common_to_alphabetical_key(self._decryption_key)

    def reset(self):
        """Reset the solver to its initial state.

        Set the decryption key to its initial state, effectively starting over.
        """

        self._decryption_key = self._get_initial_key(self._ciphertext)
