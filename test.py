#!/usr/bin/env python3

from magicimport import magicimport

flask = magicimport("flask")
tqdm = magicimport("tqdm")
tornado = magicimport("tornado", version = "4.5")

print("imported:")

print(flask, "version:", flask.__version__)
print(tqdm, "version:", tqdm.__version__)
print(tornado, "version:", tornado.version)
