#!/usr/bin/env python
# encoding: utf-8

import os
import sys

from cipher_solver.simple import SimpleSolver


def main():
    script_name = os.path.basename(sys.argv[0])

    if len(sys.argv) != 2:
        sys.exit(f"Incorrect arguments. Usage: {script_name} <path_to_ciphertext_file>")

    input_file = sys.argv[1]

    with open(input_file) as f:
        ciphertext = f.read().strip()

    s = SimpleSolver(ciphertext)

    print(f"\nCiphertext:\n{ciphertext}")

    s.solve()

    print(f"\nPlaintext:\n{s.plaintext()}\n")
