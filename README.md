# Substitution Cipher Solvers

### Algorithms for solving substitution ciphers

This is a collection of Python implementations of fast algorithms for solving
[substitution ciphers](https://en.wikipedia.org/wiki/Substitution_cipher) based on
various scientific papers. Currently included are:

* [“A Fast Method for the Cryptanalysis of Substitution Ciphers”](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.55.89&rep=rep1&type=pdf)  
  by Thomas Jakobsen

#### API

```python
class SimpleSolver:
    """Simple substitution cipher solver."""

    def __init__(self, ciphertext):
        """Create new solver.

        This creates a new simple cipher solver from an initial ciphertext.
        """

    def solve(self):
        """Run the solver."""

    def plaintext(self):
        """Return the current plaintext solution."""

    def reset(self):
        """Discard the current solution and reset the solver."""
```
See the [documentation]() for full description of methods and their parameters.

#### Usage

```python
from simple import SimpleSolver

# Solve a cipher.
h = SimpleSolver("uknkgmhksztkmexmpbxtgxesxe")
h.solve()
print(h.plaintext())  # "iamalreadyfarnorthoflondon"

# Solve a new cipher.
h = SimpleSolver("keskvuakgluepbhvpmhhpvxtwhphmvydmrbuthhgkfxgsexmpbhmeymhhoh")
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
solve.py [--type=simple] <path_to_ciphertext_file>
```

#### Running tests

`make test`

#### Generating documentation

The documentation is generated from code using [pdoc3](https://pdoc3.github.io/pdoc/):

`make docs`
