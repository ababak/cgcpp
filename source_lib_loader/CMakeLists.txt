# docker run --rm -it -v "$(pwd -W):c:/source" -v "$(pwd -W)/../out:c:/out" ababak/cgcpp

cmake_minimum_required (VERSION 3.16)
find_package (init)

project (lib_loader)
set (SRC "lib_loader.cpp")
if (WIN32)
    set (CMAKE_SHARED_LIBRARY_SUFFIX_CXX ".pyd")
endif (WIN32)
build_python_module (3.9 "Release")
build_python_module (3.10 "Release")
build_python_module (3.11 "Release")

message (STATUS "CMAKE_INSTALL_PREFIX is ${CMAKE_INSTALL_PREFIX}")
