#!/usr/bin/env python3

import importlib
import json
import os
import sys

PIP = "pip%d" % sys.version_info.major
PYTHON = sys.executable
BASH = "/bin/bash"

try:
    from importlib.metadata import version as get_version
except ImportError:
    def get_version(module_name):
        m = importlib.import_module(module_name)
        return m.__version__ if "__version__" in dir(m) else m.version

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
        if version is not None and get_version(name) != version:
            raise ImportError("wrong version: expected %s got %s" % (version, get_version(name)))
        out = importlib.import_module(name)

    except ImportError:
        print("installing %s ..." % name, file = sys.stderr)
        install_target = name
        if version is not None:
            install_target += "==" + version
        os.system("%s -c \"source %s && %s install %s\"" % (BASH, os.path.join("venv", "bin", "activate"), PIP, install_target))

        importlib.invalidate_caches()
        out = importlib.import_module(name)
        out = importlib.reload(out)

        if version is not None and get_version(name) != version:
            raise ImportError("wrong version: expected %s and tried very hard to install it but still got %s" % (version, get_version(name)))

    return out
