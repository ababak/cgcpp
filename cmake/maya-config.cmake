# (c) Andriy Babak 2020-2021
# 
# date: 07/09/2020
# modified: 28/05/2021 16:41:00
# 
# Author: Andriy Babak
# e-mail: ababak@gmail.com
# ------------------------------
# description: cmake Maya config
# ------------------------------


set (MAYA_LOCATION "C:/autodesk/Maya${MAYA_VERSION}")
set (Maya_INCLUDE_DIRS "${MAYA_LOCATION}/include")
set (Maya_LIBRARY_DIRS "${MAYA_LOCATION}/lib")
set (Maya_LIBRARIES OpenMaya Foundation)

message (STATUS "MAYA_VERSION = ${MAYA_VERSION}")
message (STATUS "MAYA_LOCATION = ${MAYA_LOCATION}")
message (STATUS "Maya_INCLUDE_DIRS = ${Maya_INCLUDE_DIRS}")
message (STATUS "Maya_LIBRARIES = ${Maya_LIBRARIES}")
