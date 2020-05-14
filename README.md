# Substitution Cipher Solver

### Algorithm for solving substitution ciphers

This is Python implementation of the algorithm for solving
[simple, monoalphabetic substitution ciphers](https://en.wikipedia.org/wiki/Substitution_cipher#Simple_substitution)
described in the paper
[“A Fast Method for the Cryptanalysis of Substitution Ciphers”](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.55.89&rep=rep1&type=pdf)
by Thomas Jakobsen.

#### API

```python
class SimpleSolver:
    """Simple substitution cipher solver."""

    def __init__(self, ciphertext):
        """Create new solver.

        Creates a new cipher solver from an initial ciphertext.
        """

    def solve(self):
        """Solve the cipher.

        Run the solver and save the resulting decryption key.
        """

    def plaintext(self):
        """Return a plaintext using the current decryption key."""

    def reset(self):
        """Reset the solver to its initial state.

        Set the decryption key to its initial state, effectively starting over.
        """
```
See the [documentation](html/markmag-ovn7) for full description of methods and their parameters.

#### Requirements

* numpy

#### Usage

```python
from simple import SimpleSolver

# Solve a cipher.
h = SimpleSolver("uknkgmhksztkmexmpbxtgxesxe")
h.solve()
print(h.plaintext())  # "iamalreadyfarnorthoflondon"

h.reset()  # Discard current solution to start over.
h.solve()
print(h.plaintext())  # We have an alternative solution now.
```

Note, however, that the above ciphertext is too short to give any meaningful results.
A length of at least 300 letters is usually necessary to solve a cipher. See below for
an example using an included sample text.

#### CLI

A simple command-line interface is included. To solve a cipher, put it into a text file
using whatever alphabet is suitable, and run:

```bash
python solve.py <path_to_ciphertext_file>
```

Example:

```bash
python solve.py texts/26_char_key/ciphertexts/ciphertext_frankenstein_sample.txt
```

#### Running tests

Run all tests:

`make test`

Check coverage:

Requires the `coverage` package.

`make coverage`

#### Generating documentation

Requires the `pdoc3` package.

`make docs`
