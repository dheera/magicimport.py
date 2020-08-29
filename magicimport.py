#!/usr/bin/env python3

import importlib
import json
import os
import sys

try:
    from importlib.metadata import version as get_version
except ImportError:
    def get_version(module_name):
        module = importlib.__import__(module_name)
        if "__version__" in dir(module):
            return module.__version__
        if "version" in dir(module):
            return module.version
        if "VERSION" in dir(module):
            return module.VERSION
        return Exception("could not get version number of %s" % module_name)

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

with os.popen("%s -c \"source %s && %s -c \'import json, os; print(json.dumps(dict(os.environ)))\'\"" % (
        BASH,
        os.path.join("venv", "bin", "activate"),
        PYTHON,
    )) as p:
    venv_environ = json.loads(p.read())
    for key in venv_environ:
        os.environ[key] = venv_environ[key]

python_lib_dir = os.listdir(os.path.join("venv", "lib"))[0]
sys.path.insert(0, os.path.join("venv", "lib", python_lib_dir, "site-packages"))

def magicimport(name, version = None):
    try:
        if version is not None and importlib.metadata.version(name) != version:
            raise ImportError("wrong version: expected %s got %s" % (version, importlib.metadata.version(name)))
        out = importlib.__import__(name)

    except ImportError:
        print("installing %s ..." % name, file = sys.stderr)
        install_target = name
        if version is not None:
            install_target += "==" + version
        os.system("%s -c \"source %s && %s install %s\"" % (BASH, os.path.join("venv", "bin", "activate"), PIP, install_target))
        out = importlib.__import__(name)

        if version is not None and importlib.metadata.version(name) != version:
            raise ImportError("wrong version: expected %s and tried very hard to install it but still got %s" % (version, importlib.metadata.version(name)))

    return out
