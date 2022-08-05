# docker run --rm -v "$(pwd -W):c:/source" -v "$(pwd -W)/../out:c:/out" -v "C:/Program Files/Autodesk:c:/autodesk" ababak/cgcpp

cmake_minimum_required (VERSION 3.2)
find_package (init)

project (maya_module)
set (SRC "maya_module.cpp")
message (STATUS "Building module for Maya 2020")
build_maya_module (2020 "Release")
message (STATUS "Building module for Maya 2022")
build_maya_module (2022 "Release")
message (STATUS "Building module for Maya 2023")
build_maya_module (2023 "Release")
