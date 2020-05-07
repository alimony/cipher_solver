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
