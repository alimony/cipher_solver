#!/usr/bin/env python
# encoding: utf-8

# solve.py [--type=simple] <path_to_ciphertext_file>

import sys

from simple import SimpleSolver

SOLVERS = {
    "simple": SimpleSolver,
}

cipher_type = "simple"

for arg in sys.argv:
    if "--type" in arg:
        _, cipher_type = arg.split("=")

if cipher_type not in SOLVERS:
    sys.exit(f'Unknown cipher type "{cipher_type}"')

solver_class = SOLVERS[cipher_type]

input_file = sys.argv[-1]

with open(input_file) as f:
    ciphertext = f.read().strip()

s = solver_class(ciphertext)

print(f"Ciphertext:\n{ciphertext}")

s.solve()

print(f"Plaintext:\n{s.plaintext()}")
