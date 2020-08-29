#!/usr/bin/env python3

import importlib
import json
import os
import sys
from pprint import pprint

PIP = "pip"
PYTHON = "python"
BASH = "/bin/bash"

try:
    import virtualenv
except ImportError:
    print("installing virtualenv ...", file = sys.stderr)
    os.system("%s install virtualenv" % PIP)
    import virtualenv

if not os.path.exists("venv"):
    print("creating virtualenv venv ...", file = sys.stderr)
    os.system("%s -m virtualenv venv" % PYTHON)

with os.popen("%s -c \"source %s; %s -c \'import json, os; print(json.dumps(dict(os.environ)))\'\"" % (
        BASH,
        os.path.join("venv", "bin", "activate"),
        PYTHON,
    )) as p:
    venv_environ = json.loads(p.read())
    for key in venv_environ:
        os.environ[key] = venv_environ[key]

python_lib_dir = os.listdir(os.path.join("venv", "lib"))[0]
sys.path.append(os.path.join("venv", "lib", python_lib_dir, "site-packages"))

def magicimport(name):
    try:
        out = importlib.__import__(name)
    except ImportError:
        print("installing %s ..." % name, file = sys.stderr)
        os.system("%s -c \"source %s; %s install %s\"" % (BASH, os.path.join("venv", "bin", "activate"), PIP, name))
        out = importlib.__import__(name)

    return out
