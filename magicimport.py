#!/usr/bin/env python3

import importlib
import json
import os
import sys

try:
    import virtualenv
except ImportError:
    print("installing virtualenv ...", file = sys.stderr)
    os.system("pip install virtualenv")
    import virtualenv

if not os.path.exists("venv"):
    print("creating virtualenv venv ...", file = sys.stderr)
    os.system("python -m virtualenv venv")

with os.popen("python -c \"import json, os; print(json.dumps(dict(os.environ)))\"") as p:
    venv_environ = json.loads(p.read())
    for key in venv_environ:
        os.environ[key] = venv_environ[key]

def magicimport(name):
    try:
        out = importlib.__import__(name)
    except ImportError:
        print("installing %s ..." % name, file = sys.stderr)
        os.system("bash -c \"source venv/bin/activate; pip install %s\"" % name)
        out = importlib.__import__(name)

    return out
