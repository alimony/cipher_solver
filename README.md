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

    def __init__(self, ciphertext, lang="en", timeout=None):
        """Create new solver.

        This creates a new homophonic cipher solver from an initial ciphertext, and
        optionally a specified language. If a timeout is passed, the solver will stop
        when that many seconds have passed.
        """

    def set_timeout(self, timeout):
        """Set the solver timeout.

        When the timeout is not None, the solver will run for a certain amount of time
        instead of until a certain solution quality. This is useful if an initial
        solution is not considered good enough. The solver can then be run over and over
        again with a timeout for as many times as needed.
        """

    def solve(self):
        """Run the solver.

        Run the solver until the solution quality does not improve. This is determined
        by looking at the score of the solution over time. If a timeout was passed when
        creating the solver, it will instead stop at that time, regardless of solution.
        """

    def get_cleartext(self):
        """Return the current cleartext solution."""

    def reset(self):
        """Discard the current solution and reset the solver.

        This will return the solver to an unsolved state, but with preserved language
        and timeout parameters, useful for starting over.
        """
```
See the [documentation](html/homophonic.html) for full description of methods and their
parameters.

#### Usage

```python
from homophonic import HomophonicSolver

h = HomophonicSolver("F7EZ5F UC2 1DR6 M9PP 0E 6CZ SD4UP1")
h.solve()

print(h.get_cleartext())  # "DEFEND THE EAST WALL OF THE CASTLE"

# Try solving with the assumption that cleartext is in Swedish, and stop after a minute.
h = HomophonicSolver("VPk|1LTG2dNp+B(#O%DWY.<*Kf)By:cM+UZG", lang="sv")

print(h.get_cleartext())  # None, since solver hasn't run with the new ciphertext yet.

h.solve()

h.set_timeout(60.0)
h.solve()  # Run for another minute.

print(h.get_cleartext())  # We might have a good solution now... or not.

h.reset()  # Discard current solution to start over.
h.set_timeout(None)
h.solve()
```

#### CLI

A simple command-line interface is included. To solve a cipher, put it into a text file
using whatever alphabet is suitable, and run:

```bash
solve.py [--lang=en] <path_to_ciphertext_file>
```

The currently best-scored solution is printed every ten seconds and the program runs
indefinitely until interrupted. The `lang` argument is optional and allows you to base
the cryptanalysis on statistics specific to that language, identified by its
[two-letter ISO 639-1 code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes).

#### Running tests

`python -m unittest discover`

#### Generating documentation

The documentation is generated from code using [pdoc3](https://pdoc3.github.io/pdoc/):

`pdoc --html --force homophonic`
