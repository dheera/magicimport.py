#!/usr/bin/env python3

from __future__ import print_function

import importlib
import json
import os
import sys

PIP = "pip%d" % sys.version_info.major
PYTHON = sys.executable
BASH = "/bin/bash"

if "reload" not in dir(importlib):
    try:
        # old python polyfill
        import imp
        importlib.reload = imp.reload
    except ImportError:
        # old old python polyfill
        importlib.reload = reload

try:
    from importlib.metadata import version as get_version
except ImportError:
    def get_version(module_name):
        m = importlib.import_module(module_name)
        return m.__version__ if "__version__" in dir(m) else m.version

if os.system("virtualenv --version > /dev/null") != 0:
    print("virtualenv not found, installing ...", file = sys.stderr)
    if os.system("%s install virtualenv" % PIP) != 0:
        raise Exception("Could not install virtualenv. Maybe %s is missing? That's the one thing I won't try to auto-install." % PIP)

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

def compare_version(target, actual):
    """
    Return true if it is a version match.
    2, 2 -> True
    2, 2.4 -> True
    2, 2.4.1 -> True
    2.4, 2.4.1 -> True
    2.4.1, 2.4.1 -> True

    2.4.1, 2.4 -> False
    2.4.1, 2.4.0 -> False
    2.4.1, 1.9.0 -> False

    etc.
    """

    if len(target.split(".")) < len(actual.split(".")):
        target = target + "."
    return actual.startswith(target)

def magicimport(name, version = None):
    try:
        if version is not None and not compare_version(version, get_version(name)):
            raise ImportError("Wrong version: expected %s got %s" % (version, get_version(name)))
        out = importlib.import_module(name)

    except ImportError:
        print("installing %s ..." % name, file = sys.stderr)
        install_target = name
        if version is not None:
            install_target += "==" + version
        os.system("%s -c \"source %s && %s install %s\"" % (BASH, os.path.join("venv", "bin", "activate"), PIP, install_target))

        if "invalidate_caches" in dir(importlib):
            importlib.invalidate_caches()
        out = importlib.import_module(name)
        out = importlib.reload(out)

        if version is not None and not compare_version(version, get_version(name)):
            raise ImportError("Wrong version: expected %s and tried very hard to install it but still got %s" % (version, get_version(name)))

    return out
