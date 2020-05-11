from string import ascii_lowercase

import numpy as np
from consts import (
    DIGRAM_FREQS_ENGLISH,
    ENGLISH_LETTER_FREQUENCIES,
    RANDOM_ITERATIONS,
    STANDARD_ALPHABET_SIZE,
)


class HomophonicSolver:
    """Homophonic substitution cipher solver."""

    def __init__(self, ciphertext):
        """Create new solver.

        This creates a new homophonic cipher solver from an initial ciphertext.

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

        alphabet = str(sorted(list(set(ciphertext))))
        self._alphabet = (
            alphabet if len(alphabet) > STANDARD_ALPHABET_SIZE else ascii_lowercase
        )

        # This corresponds to K in the paper.
        self._putative_plaintext_key = None

        # This corresponds to D_C in the paper and never changes.
        self._ciphertext_digram_frequencies = self._get_digram_frequencies(ciphertext)

        # This corresponds to D_P in the paper.
        self._plaintext_digram_frequencies = None

        alphabet_size = self._get_num_distinct_letters(ciphertext)
        self._frequency_distribution = self._get_frequency_distribution(alphabet_size)

        self._best_key = None
        self._best_initial_key = None

    def _get_frequency_distribution(self, alphabet_size):
        """Return frequency distribution based on alphabet size. The returned numpy
        array contains the number of occurrences in alphabetical order."""

        # Alphabet size must be at least 26.
        if alphabet_size < STANDARD_ALPHABET_SIZE:
            alphabet_size = STANDARD_ALPHABET_SIZE

        # Assume each letter will be mapped at least once.
        tmp_distribution = [1] * STANDARD_ALPHABET_SIZE

        frequencies = list(ENGLISH_LETTER_FREQUENCIES.values())

        # If there are more letters than in the English alphabet, distribute them over
        # the entire range according to letter frequencies.
        for _ in range(alphabet_size - STANDARD_ALPHABET_SIZE):
            max_freq = 0
            for j in range(STANDARD_ALPHABET_SIZE):
                tmp = tmp_distribution[j] + 1
                tmp_freq = frequencies[j] / tmp
                if tmp_freq > max_freq:
                    max_freq = tmp_freq
                    max_index = j
            tmp_distribution[max_index] += 1

        # Just make sure the distribution still adds up to the alphabet size.
        s = sum(tmp_distribution)
        if s != alphabet_size:
            raise Exception(
                f"Frequency distribution mismatch, distribution adds up to {s} instead of {alphabet_size}"
            )

        # Sort array alphabetically.
        distribution = np.zeros(STANDARD_ALPHABET_SIZE)
        letters_by_frequency = ENGLISH_LETTER_FREQUENCIES.keys()
        for letter, occurrences in zip(letters_by_frequency, tmp_distribution):
            index = ascii_lowercase.index(letter)
            distribution[index] = occurrences

        return distribution

    def _get_num_distinct_letters(self, text):
        """Return the number of distinct letters in the passed text."""

        return len(set(text))

    def _get_digram_frequencies(self, text, standard_size=False):
        """Generate digram frequencies for the passed text.

        Parameters
        ----------
        text : str
            The text to generate digram frequencies for.
        standard_size : bool
            If True, create a (26 x 26) English alphabet array.
            If False, create an (n x n) array where n is the number of distinct chars.

        Returns
        -------
        digram_frequencies : numpy.array
            An array of digram frequencies indexed by [first][second] letter.

        Raises
        ------
        ValueError
            If the passed text is not a string, or less than two letters.
        """

        if not isinstance(text, str):
            raise ValueError(f"{text} is not a string.")

        if len(text) < 2:
            raise ValueError(f"{text} must be at least two letters.")

        n = STANDARD_ALPHABET_SIZE if standard_size else len(set(text))
        frequencies = np.zeros((n, n))

        text_length = len(text)

        if standard_size:
            for i in range(0, text_length - 1):
                a = ascii_lowercase.index(text[i].lower())
                b = ascii_lowercase.index(text[i + 1].lower())
                frequencies[a, b] += 1

        # Replace each entry with a percentage of the total text length, to get the same
        # format as the English digram frequencies.
        rows, columns = frequencies.shape
        for i in range(rows):
            for j in range(columns):
                frequencies[i, j] = frequencies[i, j] / n ** 2

        return frequencies

    def _update_plaintext_digram_frequencies(self, key):
        """Update the current putative plaintext digram frequencies using the initially
        saved ciphertext digram frequencies and the passed key."""

        pass

    def _score(self, matrix1, matrix2=DIGRAM_FREQS_ENGLISH):
        if matrix1.shape != matrix2.shape:
            raise ValueError("Digram frequency matrices must have the same dimensions")

        return abs(matrix1 - matrix2).sum()

    def _outer_hill_climb(self):
        """Run the outer hill climb that determines the optimal distribution of
        characters when mapping the ciphertest alphabet to the plaintext alphabet."""

        # OuterHillClimb
        # global K = bestInitKey = bestKey = NULL
        # parse ciphertext to determine DC
        # initialize na, nb, ..., nz as in Table 7
        # (m1, m2, ..., m26) = (na, nb, ..., nz)
        # bestScore = RandomInitialKey(m1, m2, ..., m26)
        # bestKey = bestInitKey
        # for i = 1 to 25
        #     for j = 1 to 26 − i
        #         (m'1, m'2,...,m'26) = (m1, m2, ..., m26)
        #         outerSwap(m'[j], m'[j+i])
        #         score = RandomInitialKey(m'1, m'2, ..., m'26)
        #         if score < bestScore then
        #             (m1, m2, ..., m26) = (m'1, m'2, ..., m'26)
        #             bestScore = score
        #             bestKey = bestInitKey
        #         else
        #             (m'1, m'2, ..., m'26) = (m1, m2, ..., m26)
        #             outerSwap(m'[j+i], m'[j])
        #             score = RandomInitialKey(m'1, m'2, ..., m'26)
        #             if score < bestScore then
        #                 (m1, m2, ..., m26) = (m'1, m'2, ..., m'26)
        #                 bestScore = score
        #                 bestKey = bestInitKey
        #             end if
        #         end if
        #     next j
        # next i
        # return bestKey

        distribution = np.copy(self._frequency_distribution)

        best_score = self._random_initial_key(distribution)
        self._best_key = self._best_initial_key
        for i in range(STANDARD_ALPHABET_SIZE - 1):
            for j in range(STANDARD_ALPHABET_SIZE - i):
                tmp_distribution = np.copy(distribution)
                # Outer swap:
                tmp_distribution[j] += 1
                tmp_distribution[j + i] -= 1
                score = self._random_initial_key(tmp_distribution)
                if score < best_score:
                    distribution = np.copy(tmp_distribution)
                    best_score = score
                    self._best_key = self._best_initial_key
                else:
                    tmp_distribution = np.copy(distribution)
                    tmp_distribution[j + i] += 1
                    tmp_distribution[j] -= 1
                    score = self._random_initial_key(tmp_distribution)
                    if score < best_score:
                        distribution = np.copy(tmp_distribution)
                        best_score = score
                        self._best_key = self._best_initial_key

    def _key_from_distribution(distribution):
        """Return a key that satisfies the given distribution."""

        pass

    def _random_initial_key(self, distribution):
        # RandomInitialKey(na, nb, ..., nz)
        # bestInitScore = ∞
        # for r = 1 to R
        #     randomly initialize K = (k1, k2, ..., kn) satisfying na, nb, ..., nz
        #     DP = digram matrix from DC and K
        #     initScore = InnerHillClimb(DP)
        #     if initScore < bestInitScore then
        #         bestInitScore = initScore
        #         bestInitKey = K
        #     end if
        # next r
        # return bestInitScore

        best_initial_score = float("inf")

        for _ in range(RANDOM_ITERATIONS):
            k = self._key_from_distribution(distribution)
            self._putative_plaintext_key = k
            self._update_plaintext_digram_frequencies(k)
            initial_score = self._inner_hill_climb(self._plaintext_digram_frequencies)
            if initial_score < best_initial_score:
                best_initial_score = initial_score
                self._best_initial_key = k

        return best_initial_score

    def _inner_hill_climb(self):
        # InnerHillClimb(DP)
        # innerScore = d(DP, E)
        # for i = 1 to n − 1
        #     for j = 1 to n − i
        #         K' = K
        #         swap(k'[j], k'[j+1])
        #         D' = digram matrix for K' using DP and DC
        #         if d(D', E) < innerScore then
        #             innerScore = d(D', E)
        #             K = K'
        #             DP = D'
        #         end if
        #     next j
        # next i
        # return innerScore

        pass

    def solve(self):
        """Run the solver."""

        pass

    def plaintext(self):
        """Return the current plaintext solution.

        Returns
        -------
        plaintext : str or None
            The current plaintext solution, or None of solver hasn't run.
        """

        pass

    def reset(self):
        """Discard the current solution and reset the solver."""

        pass
