# magicimport.py

We're making L5 autonomous cars, but for some reason we can't make L5 autonomous software that "just works".

The idea of magicimport.py is to allow an arbitrary piece of Python code to fetch its own dependencies and versions at runtime and "just run", no questions asked, without fuss.
Behind the hood it uses virtualenv to create a virtual environment and install its dependencies there without messing with your system Python packages.

The ONLY package it will install to your system (and in user-space, only) is virtualenv itself, if you don't already have it.

Normally you would do this:
```
import numpy
```
and of course your system may complain that numpy wasn't found.

With magicimport.py you can do this:
```
from magicimport import magicimport
numpy = magicimport("tornado")
```
and BAM, you have numpy, no qusetions asked.

You can even specify a version number that you would like, e.g.
```
from magicimport import magicimport
numpy = magicimport("tornado", version = "4.5")
```
and you will get that exact version.

Enjoy!
