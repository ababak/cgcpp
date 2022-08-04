# docker run --rm -v "$(pwd -W):c:/source" -v "$(pwd -W)/../out:c:/out" cgcpp

cmake_minimum_required (VERSION 3.16)
find_package (init)

project (lib_exception)
set (SRC "lib_exception.cpp")
build_python_module (2.7 "Release")
build_python_module (3.9 "Release")

message (STATUS "CMAKE_INSTALL_PREFIX is ${CMAKE_INSTALL_PREFIX}")
