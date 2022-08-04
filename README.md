# Computer Graphics C++ (cgcpp)
A universal solution for common needs in C++ in computer graphics software.

### Supports
- Python 2.7 on Windows
- Python 3.9 on Windows
- Autodesk Maya 2019-2023 on Windows
- SideFX Houdini 19.0-19.5 on Windows

Support for other platforms and other CG applications may come later.

### Features
- Build inside a docker container (isolated predictable environment)
- Call library C++ functions from Python
- Dynamically reload modified libraries
- Throw Python exceptions from C++

## Installation
Install in your virtual environment:

    python -m pip install git+https://github.com/ababak/cgcpp.git

## Build the examples

    mkdir out
    python -m cgcpp examples/source_exception --out ./out
    python -m cgcpp examples/source_maya --out ./out --maya

## Test built examples
Should throw `AttributeError: Some error` exception:

    python -c 'import cgcpp;cgcpp.call(lib="out/lib_exception", func="call")'
