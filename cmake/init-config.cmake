# (c) Andriy Babak 2020-2024
# 
# date: 08/09/2020
# modified: 20/04/2023 15:21:22
# 
# Author: Andriy Babak
# e-mail: ababak@gmail.com
# ------------------------------
# description: cmake init config
# ------------------------------


set (CMAKE_MODULE_PATH "C:/cmake")

include(compiler)
include(build_functions)

message (STATUS "CMake version: ${CMAKE_VERSION}")

set(Boost_USE_STATIC_LIBS ON)
add_definitions(-DBOOST_PYTHON_STATIC_LIB)
set (Python_FIND_STRATEGY "LOCATION")

if (EXISTS "C:/out")
    set (CMAKE_INSTALL_PREFIX "C:/out" CACHE PATH "..." FORCE)
else ()
    set (CMAKE_INSTALL_PREFIX "C:/source" CACHE PATH "..." FORCE)
endif ()
message (STATUS "CMake install directory: ${CMAKE_INSTALL_PREFIX}")
