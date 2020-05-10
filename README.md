# Homophonic Solver

### An algorithm for solving homophonic substitution ciphers

This is a Python implementation of the nested hill climb algorithm for solving
[homophonic substitution ciphers](https://en.wikipedia.org/wiki/Substitution_cipher#Homophonic_substitution)
described in the paper
[“Efficient Cryptanalysis of Homophonic Substitution Ciphers”](http://www.cs.sjsu.edu/~stamp/RUA/homophonic.pdf)
by Amrapali Dhavare, Richard M. Low, and Mark Stamp.

#### API

```python
class HomophonicSolver:
    """Homophonic substitution cipher solver."""

    def __init__(self, ciphertext):
        """Create new solver.

        This creates a new homophonic cipher solver from an initial ciphertext.
        """

    def solve(self, random_iterations=40):
        """Run the solver."""

    def plaintext(self):
        """Return the current plaintext solution."""

    def reset(self):
        """Discard the current solution and reset the solver."""
```
See the [documentation](html/homophonic.html) for full description of methods and their
parameters.

#### Usage

```python
from homophonic import HomophonicSolver

# Solve a cipher.
h = HomophonicSolver("F7EZ5FUC21DR6M9PP0E6CZ SD4UP1")
h.solve()
print(h.plaintext())  # "DEFENDTHEEASTWALLOFTHECASTLE"

# Solve a new cipher.
h = HomophonicSolver("VPk|1LTG2dNp+B(#O%DWY.<*Kf)By:cM+UZG")
print(h.plaintext())  # None, since solver hasn't run yet.
h.solve()
print(h.plaintext())  # We might have a good solution now... or not.

h.reset()  # Discard current solution to start over.
h.solve()
print(h.plaintext())  # We have an alternative solution now.
```

#### CLI

A simple command-line interface is included. To solve a cipher, put it into a text file
using whatever alphabet is suitable, and run:

```bash
solve.py [--lang=en] <path_to_ciphertext_file>
```

#### Running tests

`make test`

#### Generating documentation

The documentation is generated from code using [pdoc3](https://pdoc3.github.io/pdoc/):

`make docs`
