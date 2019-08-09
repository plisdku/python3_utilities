"""
Something by
Paul Hansen
paul.c.hansen@gmail.com
"""

import os, sys
import subprocess

def _shell_that_path(cmd, path, directory=False):
    if hasattr(path, "__file__"):
        path = path.__file__
    elif hasattr(path, "__code__"):
        path = path.__code__.co_filename

    if directory:
        path = os.path.dirname(path)
    subprocess.run([cmd, path])
    
def open_module(module, directory=False):
    _shell_that_path("open", module, directory)
    
def bbedit_module(module, directory=False):
    _shell_that_path("bbedit", module, directory)