# Substitution Cipher Solver

### Algorithm for solving simple, monoalphabetic substitution ciphers

This is Python implementation of the algorithm for solving
[simple, monoalphabetic substitution ciphers](https://en.wikipedia.org/wiki/Substitution_cipher#Simple_substitution)
described in the paper
[“A Fast Method for the Cryptanalysis of Substitution Ciphers”](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.55.89&rep=rep1&type=pdf)
by Thomas Jakobsen. The main difference from the paper is that random key swaps are used
instead of a deterministic series of swaps since it yields better results, but the
original method is included and can be used as an option.

#### Installing

    pip install cipher_solver

#### API

```python
class SimpleSolver:
    """Simple substitution cipher solver."""

    def __init__(self, ciphertext):
        """Create new solver.

        Creates a new cipher solver from an initial ciphertext.
        """

    def solve(self, method="random"):
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
See the [documentation](https://alimony.github.io/cipher_solver/) for full description
of methods and their parameters.

#### Requirements

* numpy

#### Usage

```python
from cipher_solver.simple import SimpleSolver

# Solve a cipher.
s = SimpleSolver("U kn kgmhksz tkm exmpb xt Gxesxe.")
s.solve()
print(s.plaintext())  # "I am already far north of London."

s.reset()  # Discard current solution to start over.
s.solve()
print(s.plaintext())  # We have an alternative solution now.

print(s.decryption_key())  # "goaskbihxvrldepfwntmzqjucy"

# Solve using the original key swap method instead.
d = SimpleSolver("U kn kgmhksz tkm exmpb xt Gxesxe.", method="deterministic")
d.solve()
print(s.plaintext())
```

Note, however, that the above ciphertext is too short to give any meaningful results.
A length of at least a few hundred letters is preferred to solve a cipher. See below for
an example using an included sample text.

#### CLI

A simple command-line interface is included. To solve a cipher, put it into a text file
and run:

```bash
cipher_solver <path_to_ciphertext_file>
```

Example:

```bash
cipher_solver texts/26_char_key/ciphertexts/ciphertext_frankenstein_sample.txt
```

Since the algorithm involves [hill climbing](https://en.wikipedia.org/wiki/Hill_climbing)
and randomness you might sometimes end up with complete gibberish, just run the script
again and the next result should be better.

#### Running tests

    make test

#### Checking coverage

    make coverage

(Requires the `coverage` package.)

#### Generating documentation

    make docs

(Requires the `pdoc3` package.)
