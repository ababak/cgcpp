"""
(c) Andriy Babak 2021

date: 31/05/2021
modified: 03/06/2021 16:37:24

Author: Andriy Babak
e-mail: ababak@gmail.com
------------------------------
description: CG C++ Support module
Containerized builds and runtime loading
------------------------------
"""

import os
import inspect
import platform
from . import build
from ._version import __version__

__copyright__ = "(c) Andriy Babak 2021"


def _get_library_path(lib_path):
    """
    Try to guess a full library path
    """
    lib_dir = os.path.dirname(lib_path)
    lib_name = os.path.basename(lib_path)
    lib_name, lib_ext = os.path.splitext(lib_name)
    local_platform = platform.system().lower()
    if local_platform == "windows":
        lib_ext = ".dll"
    elif local_platform == "linux":
        lib_ext = ".so"
    else:
        raise EnvironmentError("Unsupported platform: %s", local_platform)
    if not lib_dir:
        # get call stack frames
        frames = inspect.stack(0)
        # should be the third frame
        # 0: this function
        # 1: this module"s "call" function
        # 2: the caller
        if len(frames) > 2:
            path = frames[2][1]
            if path:
                lib_dir = os.path.dirname(path)
    full_lib_path = os.path.join(os.path.abspath(lib_dir), lib_name + lib_ext)
    if not os.path.isfile(full_lib_path):
        try:
            import maya.cmds as cmds
        except ImportError:
            pass
        else:
            maya_version = str(cmds.about(v=True))
            full_lib_path = os.path.join(
                os.path.abspath(lib_dir), lib_name + "_maya" + maya_version + lib_ext
            )
            if os.path.isfile(full_lib_path):
                return full_lib_path
        raise AttributeError('Library not found: "' + full_lib_path + '"')
    return full_lib_path


def call(*args, **kwargs):
    """
    Call an external function from dynamically loaded library
    Arguments:
        lib (str) - full library path ("/some/lib/lib.so") or library name ("lib")
        func (str) - function name
        All the arguments get passed to an exported function from the library
    Usage:
        ret = cpp.call("some argument", some_named_argument=42, lib="/lib/path.so", func="custom")
    """
    from . import lib_loader

    lib_path = kwargs.get("lib")
    func_name = kwargs.get("func")
    if not lib_path or not func_name:
        raise AttributeError('Invalid usage. Expected arguments: "lib", "func"')
    modified_kwargs = dict(kwargs)
    modified_kwargs["lib"] = _get_library_path(lib_path)
    return lib_loader.call(*args, **modified_kwargs)
