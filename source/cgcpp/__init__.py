"""
(c) Andriy Babak 2021-2024

date: 31/05/2021
modified: 30/05/2024 10:40:19

Author: Andriy Babak
e-mail: ababak@gmail.com
------------------------------
description: CG C++ Support module
Containerized builds and runtime loading
------------------------------
"""

import os
import sys
import inspect
import platform
from ._version import __version__
from . import build

__copyright__ = "(c) Andriy Babak 2021-2024"

lib_loader_name = "lib_loader"
lib_suffix = "_python{major}{minor}".format(
    major=sys.version_info.major,
    minor=sys.version_info.minor,
)
lib_loader_path = "{folder}/{name}{suffix}.pyd".format(
    folder=os.path.dirname(__file__), name=lib_loader_name, suffix=lib_suffix
)
try:
    import importlib.util

    spec = importlib.util.spec_from_file_location(lib_loader_name, lib_loader_path)
    lib_loader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lib_loader)
except ImportError:
    import imp

    with open(lib_loader_path, "rb") as f:
        lib_loader = imp.load_module(
            "lib_loader", f, lib_loader_path, (".pyd", "rb", 3)
        )


def get_library_path(lib_path, extra_frames=0):
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
        frame = 1 + extra_frames
        # should be the third frame
        # 0: this function
        # 1: this module"s "call" function
        # 2: the caller
        if len(frames) > frame:
            path = frames[frame][1]
            if path:
                lib_dir = os.path.dirname(path)
    full_lib_path = os.path.join(os.path.abspath(lib_dir), lib_name + lib_ext)
    variants = [lib_name + lib_ext, lib_name + lib_suffix + lib_ext]
    try:
        from maya import cmds
    except ImportError:
        pass
    else:
        maya_version = str(cmds.about(v=True))
        maya_suffix = "_maya" + maya_version
        variants.append(lib_name + maya_suffix + lib_ext)
        variants.append(lib_name + lib_suffix + maya_suffix + lib_ext)
    try:
        import hou
        from hou import nodes
    except ImportError:
        pass
    else:
        houdini_version = os.path.splitext(hou.applicationVersionString())[0]
        houdini_suffix = "_houdini" + houdini_version
        variants.append(lib_name + houdini_suffix + lib_ext)
        variants.append(lib_name + lib_suffix + houdini_suffix + lib_ext)
    for name in variants:
        full_lib_path = os.path.join(os.path.abspath(lib_dir), name)
        if os.path.isfile(full_lib_path):
            return full_lib_path
    raise AttributeError(
        'Library not found: "{}"'.format(
            os.path.join(os.path.abspath(lib_dir), lib_name + lib_ext)
        )
    )


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
    lib_path = kwargs.get("lib")
    func_name = kwargs.get("func")
    if not lib_path or not func_name:
        raise AttributeError('Invalid usage. Expected arguments: "lib", "func"')
    modified_kwargs = dict(kwargs)
    modified_kwargs["lib"] = get_library_path(lib_path, extra_frames=1)
    return lib_loader.call(*args, **modified_kwargs)
