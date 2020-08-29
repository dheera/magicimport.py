#!/usr/bin/env python3

from magicimport import magicimport

flask = magicimport("flask")
print(flask)

tqdm = magicimport("tqdm")
print(tqdm)

tornado = magicimport("tornado", version = "4.5")
print(tornado)
