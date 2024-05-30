[![Docker Image CI](https://github.com/ababak/cgcpp/actions/workflows/docker-image.yml/badge.svg?branch=v1.4.0)](https://github.com/ababak/cgcpp/actions/workflows/docker-image.yml)

# Computer Graphics C++ (cgcpp)
A universal solution for common needs in C++ in computer graphics software.

### Supports
- Python 3.9, Boost 1.76.0 on Windows
- Python 3.10, Boost 1.80.0 on Windows
- Python 3.11, Boost 1.82.0 on Windows
- Autodesk Maya 2019-2025 on Windows *(Python 3.9 and Boost 1.76.0 in Maya 2023, Python 3.10 and Boost 1.80.0 in Maya 2024, Python 3.11 and Boost 1.82.0 in Maya 2025)*
- SideFX Houdini 19.0-19.5 on Windows *(Python 3.9 and Boost 1.76.0 in Houdini 19.5, Python 3.10 and Boost 1.80.0 in Houdini 20.0)*

Support for other platforms and other DCC applications may come later.

### Features
- Build inside a docker container (isolated predictable environment)
- Call library C++ functions from Python
- Dynamically reload modified libraries (each new call reloads the library and alows it to be updated)
- Throw Python exceptions from C++

## Installation
Install in your Windows Python virtual environment:

    python -m pip install git+https://github.com/ababak/cgcpp.git

## Build the examples

    mkdir out
    python -m cgcpp examples/source_exception --out ./out
    python -m cgcpp examples/source_maya --out ./out --maya
    python -m cgcpp examples/source_houdini --out ./out --houdini

Make sure you have Maya and Houdini versions installed in default locations that correspond to versions listed in `CMakeLists.txt`

## Test built examples
Should throw `AttributeError: Some error` exception:

    python -c 'import cgcpp;cgcpp.call(lib="out/lib_exception", func="call")'

Inside Maya:

    import cgcpp
    print(cgcpp.call(lib="out/maya_module", func="ls"))

Inside Houdini:

    import cgcpp
    print(cgcpp.call(lib="out/houdini_module", func="ls"))
