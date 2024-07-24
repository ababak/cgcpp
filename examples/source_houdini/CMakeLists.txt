# docker run --rm -v "$(pwd -W):c:/source" -v "$(pwd -W)/../out:c:/out" -v "C:/Program Files/Autodesk:c:/autodesk" ababak/cgcpp

cmake_minimum_required (VERSION 3.2)
find_package (init)

project (houdini_module)
set (SRC "houdini_module.cpp")
message (STATUS "Building module for Houdini 19.0.657")
build_houdini_module (19.0.657 "Release")
message (STATUS "Building module for Houdini 20.0.688")
build_houdini_module (20.0.688 "Release")
