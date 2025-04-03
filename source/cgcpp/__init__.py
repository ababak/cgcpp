"""
(c) Andriy Babak 2021-2025

date: 31/05/2021
modified: 03/04/2025 12:10:58

Author: Andriy Babak
e-mail: ababak@gmail.com
------------------------------
description: CG C++ Support module
Containerized builds and runtime loading
------------------------------
"""

import importlib.metadata
import importlib.util
import inspect
import os
import platform
import sys
from pathlib import Path

__version__ = importlib.metadata.version("cgcpp")
__copyright__ = "(c) Andriy Babak 2021-2025"

from . import build

lib_loader_name = "lib_loader"
lib_suffix = f"_python{sys.version_info.major}{sys.version_info.minor}"
lib_loader_path = Path(__file__).with_name(f"{lib_loader_name}{lib_suffix}.pyd")

spec = importlib.util.spec_from_file_location(lib_loader_name, lib_loader_path)
lib_loader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lib_loader)


def get_library_path(lib_path, extra_frames=0):
    """
    Try to guess a full library path
    """
    lib_path = Path(lib_path)
    lib_dir = lib_path.parent
    lib_name = os.path.basename(lib_path)
    lib_name, lib_ext = os.path.splitext(lib_path.name)
    local_platform = platform.system().lower()
    if local_platform == "windows":
        lib_ext = ".dll"
    elif local_platform == "linux":
        lib_ext = ".so"
    else:
        raise EnvironmentError(f"Unsupported platform: {local_platform}")
    if not os.path.dirname(lib_path):
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
                lib_dir = Path(path).parent
    full_lib_path = lib_dir.absolute() / f"{lib_name}{lib_ext}"
    variants = [f"{lib_name}{lib_ext}", f"{lib_name}{lib_suffix}{lib_ext}"]
    # Try to guess the host application
    try:
        from maya import cmds
    except ImportError:
        pass
    else:
        # The host application is Maya
        maya_version = cmds.about(v=True)
        maya_suffix = f"_maya{maya_version}"
        variants.append(f"{lib_name}{maya_suffix}{lib_ext}")
        variants.append(f"{lib_name}{lib_suffix}{maya_suffix}{lib_ext}")
    try:
        import hou
        from hou import nodes
    except ImportError:
        pass
    else:
        # The host application is Houdini
        houdini_version = os.path.splitext(hou.applicationVersionString())[0]
        houdini_suffix = f"_houdini{houdini_version}"
        variants.append(f"{lib_name}{houdini_suffix}{lib_ext}")
        variants.append(f"{lib_name}{lib_suffix}{houdini_suffix}{lib_ext}")
    for name in variants:
        full_lib_path = lib_dir.absolute() / name
        if full_lib_path.is_file():
            return full_lib_path
    raise AttributeError(
        f'Library not found: "{lib_dir.absolute().with_name(lib_name + lib_ext)}"'
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
    modified_kwargs["lib"] = get_library_path(lib_path, extra_frames=1).as_posix()
    return lib_loader.call(*args, **modified_kwargs)
