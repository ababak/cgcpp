[![Docker Image CI](https://github.com/ababak/cgcpp/actions/workflows/docker-image.yml/badge.svg)](https://github.com/ababak/cgcpp/actions/workflows/docker-image.yml)

# Computer Graphics C++ (cgcpp)  
A universal C++ solution for common needs in computer graphics software.

### Supported Environments  
- **Python & Boost Versions** (Windows):  
  - Python 3.9, Boost 1.76.0  
  - Python 3.10, Boost 1.80.0  
  - Python 3.11, Boost 1.82.0  
  - Python 3.12, Boost 1.85.0  
- **Autodesk Maya** (Windows):  
  - Maya 2023: Python 3.9, Boost 1.76.0  
  - Maya 2024: Python 3.10, Boost 1.80.0  
  - Maya 2025: Python 3.11, Boost 1.82.0  
  - Maya 2026: Python 3.11, Boost 1.85.0  
- **SideFX Houdini** (Windows):  
  - Houdini 19.5: Python 3.9, Boost 1.76.0  
  - Houdini 20.0: Python 3.10, Boost 1.80.0  
  - Houdini 20.5: Python 3.11, Boost 1.82.0  

Support for additional platforms and DCC applications may be added in the future.

### Features  
- **Isolated builds** inside a Docker container for a predictable environment  
- **Python-C++ integration** to call C++ functions from Python  
- **Dynamic library reloading** (updates libraries on each new call)  
- **Python exception handling** from C++  

## Installation  
Install in your Windows Python virtual environment: 

    python -m pip install git+https://github.com/ababak/cgcpp.git

or

    pip install cgcpp

## Building Examples

    mkdir out
    python -m cgcpp examples/source_exception --out ./out
    python -m cgcpp examples/source_maya --out ./out --maya
    python -m cgcpp examples/source_houdini --out ./out --houdini

Ensure you have Maya and Houdini installed in their default locations as specified in `CMakeLists.txt`

## Testing Built Examples
Should throw `AttributeError: Some error` exception:

    python -c 'import cgcpp;cgcpp.call(lib="out/lib_exception", func="call")'

Inside Maya:

    import cgcpp
    print(cgcpp.call(lib="out/maya_module", func="ls"))

Inside Houdini:

    import cgcpp
    print(cgcpp.call(lib="out/houdini_module", func="ls"))
