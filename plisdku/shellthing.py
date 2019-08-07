import os, sys
import subprocess

def _shell_that_path(cmd, path, directory=False):

    if hasattr(path, "__file__"):
        path = path.__file__

    if directory:
        path = os.path.dirname(path)
    subprocess.run([cmd, path])
    
def open_module(module, directory=False):
    _shell_that_path("open", module, directory)
    
def bbedit_module(module, directory=False):
    _shell_that_path("bbedit", module, directory)