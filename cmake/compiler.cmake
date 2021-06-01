# (c) Andriy Babak 2020-2021
# 
# date: 08/09/2020
# modified: 28/05/2021 16:41:32
# 
# Author: Andriy Babak
# e-mail: ababak@gmail.com
# ------------------------------
# description: cmake compiler settings
# ------------------------------


set(CMAKE_CXX_STANDARD 17)
if (WIN32)
    add_definitions (-DWIN64)
    add_definitions (-DBOOST_ALL_NO_LIB)
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /EHsc")
else ()
    add_definitions (-std=c++11)
    add_definitions (-fPIC)
    add_definitions (-Ofast)
    # add_definitions (-pthread)
endif ()
