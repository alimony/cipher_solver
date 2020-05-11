from abc import ABC, abstractmethod


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
