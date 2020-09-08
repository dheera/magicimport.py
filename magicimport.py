#!/usr/bin/env python3

from __future__ import print_function

import importlib
import json
import os
import random
import sys

PIP = "pip%d" % sys.version_info.major
PYTHON = sys.executable
BASH = "/bin/bash"

try:
    VENV = os.path.join(os.path.dirname(os.path.realpath(__file__)), "venv.magicimport")
except NameError:
    VENV = "venv.magicimport"

if not os.access(VENV, os.W_OK):
    VENV = "/tmp/venv.magicimport.%d" % random.randint(100000,999999)


if "reload" not in dir(importlib):
    try:
        # old python polyfill
        import imp
        importlib.reload = imp.reload
    except ImportError:
        # old old python polyfill
        importlib.reload = reload

def get_version(module_name):
    m = importlib.import_module(module_name)
    return m.__version__ if "__version__" in dir(m) else m.version

if os.system("virtualenv --version > /dev/null") != 0:
    print("virtualenv not found, installing ...", file = sys.stderr)
    if os.system("%s install virtualenv" % PIP) != 0:
        raise Exception("Could not install virtualenv. Maybe %s is missing? That's the one thing I won't try to auto-install." % PIP)

if not os.path.exists(VENV):
    print("creating virtualenv venv ...", file = sys.stderr)
    result = os.system("%s -m virtualenv %s" % (PYTHON, VENV))

with os.popen("%s -c \"source %s && %s -c \'import json, os; print(json.dumps(dict(os.environ)))\'\"" % (
        BASH,
        os.path.join(VENV, "bin", "activate"),
        PYTHON,
    )) as p:
    venv_environ = json.loads(p.read())
    for key in venv_environ:
        os.environ[key] = venv_environ[key]

python_lib_dir = os.listdir(os.path.join(VENV, "lib"))[0]
sys.path.insert(0, os.path.join(VENV, "lib", python_lib_dir, "site-packages"))

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

    if len(target.split(".")) > len(actual.split(".")):
        target = ".".join(target.split(".")[0:len(actual.split("."))])

    return actual.startswith(target)

def magicimport(name, version = None, package_name = None):
    """
    Imports a module (install it first if it doesn't exist) and returns it. How to use:
    tensorflow = magicimport("tensorflow")    # import tensorflow
    tf = magicimport("tensorflow")            # import tensorflow as tf

    # if you want a specific version:
    tf = magicimport("tensorflow", version = "2.2")

    # if the pip name isn't the same as the python name:
    cv2 = magicimport("cv2", version = "4.4.0.42", package_name = "opencv-python")
    """
    try:
        out = importlib.import_module(name)

        if version is not None and not compare_version(version, get_version(name)):
            raise ImportError("Wrong version: expected %s got %s" % (version, get_version(name)))

    except ImportError:
        print("installing %s ..." % name, file = sys.stderr)

        if package_name is not None:
            install_target = package_name
        else:
            install_target = name

        if version is not None:
            install_target += "==" + version

        os.system("%s -c \"source %s && %s install %s\"" % (BASH, os.path.join(VENV, "bin", "activate"), PIP, install_target))

        if "invalidate_caches" in dir(importlib):
            importlib.invalidate_caches()
        out = importlib.import_module(name)
        out = importlib.reload(out)

        if version is not None and not compare_version(version, get_version(name)):
            raise ImportError("Wrong version: expected %s and tried very hard to install it but still got %s" % (version, get_version(name)))

    return out
