# Computer Graphics C++ (cgcpp)
A universal solution for common needs in C++ in computer graphics software.

### Supports
- Python 2.7 on Windows
- Autodesk Maya 2019-2022 on Windows

Support for Python 3, other platforms and other CG applications will come later.

### Features
- Build inside a docker container (isolated predictable environment)
- Call library C++ functions from Python
- Dynamically reload modified libraries
- Throw Python exceptions from C++

## Installation

    python -m pip install cgcpp

## Build the examples

    python -m cgcpp examples/source_exception --out ./out
    python -m cgcpp examples/source_maya --out ./out --maya
