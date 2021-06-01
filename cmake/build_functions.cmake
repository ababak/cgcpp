# (c) Andriy Babak 2020-2021
# 
# date: 08/09/2020
# modified: 31/05/2021 11:32:22
# 
# Author: Andriy Babak
# e-mail: ababak@gmail.com
# ------------------------------
# description: cmake build functions
# ------------------------------


function(build_maya_module MAYA_VERSION PROJECT_BUILD_TYPE)
    set (CMAKE_BUILD_TYPE "${PROJECT_BUILD_TYPE}" CACHE INTERNAL "" FORCE)
    find_package (Python 2.7 REQUIRED COMPONENTS Interpreter Development)
    find_package (Boost REQUIRED COMPONENTS python27 system filesystem)
    # message (STATUS "Python_LIBRARIES = ${Python_LIBRARIES}")
    # message (STATUS "Boost_LIBRARIES = ${Boost_LIBRARIES}")
    # message (STATUS "Maya_LIBRARIES = ${Maya_LIBRARIES}")
    find_package (Maya REQUIRED)
    set (TARGET_NAME "${PROJECT_NAME}_maya${MAYA_VERSION}")
    add_library (${TARGET_NAME} SHARED ${SRC})
    set_target_properties (${TARGET_NAME} PROPERTIES PREFIX "")
    target_include_directories (
        ${TARGET_NAME}
        PRIVATE ${Python_INCLUDE_DIRS}
        PRIVATE ${Boost_INCLUDE_DIRS}
        PRIVATE ${Maya_INCLUDE_DIRS}
    )
    target_link_directories (
        ${TARGET_NAME}
        # PRIVATE ${Python_LIBRARY_DIRS}
        # PRIVATE ${Boost_LIBRARY_DIR_RELEASE}
        PRIVATE ${Maya_LIBRARY_DIRS}
    )
    target_link_libraries (
        ${TARGET_NAME}
        ${Python_LIBRARIES}
        ${Boost_LIBRARIES}
        ${Maya_LIBRARIES}
    )
    install (
        TARGETS ${TARGET_NAME} RUNTIME
        DESTINATION ${CMAKE_INSTALL_PREFIX}
    )
endfunction()


function(build_python_module PROJECT_BUILD_TYPE)
    set (CMAKE_BUILD_TYPE "${PROJECT_BUILD_TYPE}" CACHE INTERNAL "" FORCE)
    find_package (Python 2.7 REQUIRED COMPONENTS Interpreter Development)
    find_package (Boost REQUIRED COMPONENTS python27 system filesystem)
    set (TARGET_NAME "${PROJECT_NAME}")
    add_library (${TARGET_NAME} SHARED ${SRC})
    target_include_directories (
        ${TARGET_NAME}
        PRIVATE ${Python_INCLUDE_DIRS}
        PRIVATE ${Boost_INCLUDE_DIRS}
    )
    target_link_libraries (
        ${TARGET_NAME}
        ${Python_LIBRARIES}
        ${Boost_LIBRARIES}
    )
    install (
        TARGETS ${TARGET_NAME} RUNTIME
        DESTINATION ${CMAKE_INSTALL_PREFIX}
    )
endfunction()
