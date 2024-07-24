# docker run --rm -v "$(pwd -W):c:/source" -v "$(pwd -W)/../out:c:/out" ababak/cgcpp

cmake_minimum_required (VERSION 3.16)
find_package (init)

project (lib_exception)
set (SRC "lib_exception.cpp")
build_python_module (3.9 "Release")
build_python_module (3.10 "Release")
build_python_module (3.11 "Release")
build_python_module (3.12 "Release")

message (STATUS "CMAKE_INSTALL_PREFIX is ${CMAKE_INSTALL_PREFIX}")
