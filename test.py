#!/usr/bin/env python3

from magicimport import magicimport

numpy = magicimport("numpy", version = "1.17")
numba = magicimport("numba")
tornado = magicimport("tornado")
flask = magicimport("flask")
tqdm = magicimport("tqdm")

print(numpy, numba, tornado, flask, tqdm)
