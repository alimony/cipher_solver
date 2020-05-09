from string import ascii_lowercase

import numpy as np
from consts import STANDARD_ALPHABET_LENGTH


class HomophonicSolver:
    """Homophonic substitution cipher solver."""

    def __init__(self, ciphertext, lang="en", timeout=None):
        """Create new solver.

        This creates a new homophonic cipher solver from an initial ciphertext, and
        optionally a specified language. If a timeout is passed, the solver will stop
        when that many seconds have passed.

        Parameters
        ----------
        ciphertext : str
            The ciphertext to solve.

        lang : str, optional
            The language the cleartext is assumed to use.

        timeout : float, optional
            Number of seconds before stopping the solver.

        Raises
        ------
        ValueError
            If the passed language is not supported.
        """

        pass

    def set_timeout(self, timeout):
        """Set the solver timeout.

        When the timeout is not None, the solver will run for a certain amount of time
        instead of until a certain solution quality. This is useful if an initial
        solution is not considered good enough. The solver can then be run over and over
        again with a timeout for as many times as needed.

        Parameters
        ----------
        timeout : float
            Number of seconds before stopping the solver.
        """

        pass

    def solve(self):
        """Run the solver.

        Run the solver until the solution quality does not improve. This is determined
        by looking at the score of the solution over time. If a timeout was passed when
        creating the solver, it will instead stop at that time, regardless of solution.
        """

        pass

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
            raise ValueError(f"{text} must be a string.")

        if len(text) < 2:
            raise ValueError(f"{text} must be at least two letters.")

        n = STANDARD_ALPHABET_LENGTH if standard_size else len(set(text))
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

    def _outer_hill_climb(self):
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

        pass

    def _random_initial_key(self):
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

        pass

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

    def get_cleartext(self):
        """Return the current cleartext solution.

        Returns
        -------
        cleartext : str or None
            The current cleartext solution, or None of solver hasn't run.
        """

        pass

    def reset(self):
        """Discard the current solution and reset the solver.

        This will return the solver to an unsolved state, but with preserved language
        and timeout parameters, useful for starting over.
        """

        pass
