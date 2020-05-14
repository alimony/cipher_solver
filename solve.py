#!/usr/bin/env python
# encoding: utf-8

import sys

from simple import SimpleSolver


def main():
    if len(sys.argv) != 2:
        sys.exit("Incorrect arguments. Usage: solve.py <path_to_ciphertext_file>")

    input_file = sys.argv[1]

    with open(input_file) as f:
        ciphertext = f.read().strip()

    s = SimpleSolver(ciphertext)

    print(f"\nCiphertext:\n{ciphertext}")

    s.solve()

    print(f"\nPlaintext:\n{s.plaintext()}\n")


if __name__ == "__main__":
    main()
