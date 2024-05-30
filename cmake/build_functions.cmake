# (c) Andriy Babak 2020-2024
# 
# date: 08/09/2020
# modified: 30/05/2024 10:44:23
# 
# Author: Andriy Babak
# e-mail: ababak@gmail.com
# ------------------------------
# description: cmake build functions
# ------------------------------


function(build_maya_module MAYA_VERSION PROJECT_BUILD_TYPE)
    find_package (Maya REQUIRED)
    set (CMAKE_BUILD_TYPE "${PROJECT_BUILD_TYPE}" CACHE INTERNAL "" FORCE)
    if (MAYA_VERSION VERSION_LESS 2024)
        set(PYTHON_REQUESTED_VERSION 3.9)
        set(Python_ROOT_DIR "C:/Python39")
        set(BOOST_REQUESTED_VERSION 1.76.0)
        set(BOOST_ROOT "C:/local/boost_1_76_0")
    elseif (MAYA_VERSION VERSION_LESS 2025)
        set(PYTHON_REQUESTED_VERSION 3.10)
        set(Python_ROOT_DIR "C:/Python310")
        set(BOOST_REQUESTED_VERSION 1.80.0)
        set(BOOST_ROOT "C:/local/boost_1_80_0")
    elseif (MAYA_VERSION VERSION_LESS 2026)
        set(PYTHON_REQUESTED_VERSION 3.11)
        set(Python_ROOT_DIR "C:/Python311")
        set(BOOST_REQUESTED_VERSION 1.82.0)
        set(BOOST_ROOT "C:/local/boost_1_82_0")
    else ()
        message( FATAL_ERROR "Unsupported Maya version: ${MAYA_VERSION}" )
    endif ()
    message (STATUS "Python version: ${PYTHON_REQUESTED_VERSION}")
    string (REPLACE "." "" PYTHON_DOTLESS_VERSION "${PYTHON_REQUESTED_VERSION}")
    find_package (Python ${PYTHON_REQUESTED_VERSION} REQUIRED COMPONENTS Interpreter Development)
    find_package (Boost ${BOOST_REQUESTED_VERSION} EXACT REQUIRED COMPONENTS python${PYTHON_DOTLESS_VERSION} system filesystem)
    # message (STATUS "Python_LIBRARIES = ${Python_LIBRARIES}")
    # message (STATUS "Boost_LIBRARIES = ${Boost_LIBRARIES}")
    # message (STATUS "Maya_LIBRARIES = ${Maya_LIBRARIES}")
    set (TARGET_NAME "${PROJECT_NAME}_python${PYTHON_DOTLESS_VERSION}_maya${MAYA_VERSION}")
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


function(build_houdini_module HOUDINI_VERSION PROJECT_BUILD_TYPE)
    set (HFS "C:/sidefx/Houdini ${HOUDINI_VERSION}")
    # CMAKE_PREFIX_PATH must contain the path to the toolkit/cmake subdirectory of
    # the Houdini installation. See the "Compiling with CMake" section of the HDK
    # documentation for more details, which describes several options for
    # specifying this path.
    list(APPEND CMAKE_PREFIX_PATH "${HFS}/toolkit/cmake")
    find_package (Houdini REQUIRED)
    if (Houdini_VERSION VERSION_LESS 20.0)
        set(PYTHON_REQUESTED_VERSION 3.9)
        set(Python_ROOT_DIR "C:/Python39")
        set(BOOST_REQUESTED_VERSION 1.76.0)
        set(BOOST_ROOT "C:/local/boost_1_76_0")
    elseif (Houdini_VERSION VERSION_LESS 20.5)
        set(PYTHON_REQUESTED_VERSION 3.10)
        set(Python_ROOT_DIR "C:/Python310")
        set(BOOST_REQUESTED_VERSION 1.80.0)
        set(BOOST_ROOT "C:/local/boost_1_80_0")
    else ()
        message( FATAL_ERROR "Unsupported Houdini version: ${HOUDINI_VERSION}" )
    endif ()
    message (STATUS "Python version: ${PYTHON_REQUESTED_VERSION}")
    string (REPLACE "." "" PYTHON_DOTLESS_VERSION "${PYTHON_REQUESTED_VERSION}")
    set (CMAKE_BUILD_TYPE "${PROJECT_BUILD_TYPE}" CACHE INTERNAL "" FORCE)
    set (TARGET_NAME "${PROJECT_NAME}_python${PYTHON_DOTLESS_VERSION}")
    find_package (Boost ${BOOST_REQUESTED_VERSION} EXACT REQUIRED COMPONENTS python${PYTHON_DOTLESS_VERSION} system filesystem)
    add_library (${TARGET_NAME} SHARED ${SRC})
    set_target_properties (${TARGET_NAME} PROPERTIES PREFIX "")
    target_compile_features(${TARGET_NAME} PUBLIC
        cxx_auto_type
        cxx_lambdas
        cxx_nullptr
        cxx_range_for
    )
    target_include_directories (
        ${TARGET_NAME}
        PRIVATE ${Boost_INCLUDE_DIRS}
    )
    if (_houdini_platform_linux)
        # Link against Houdini libraries (including USD)
        if (DEFINED ENV{HOUDINI_HDK_LINK_GUSD})
            target_link_libraries(${TARGET_NAME}
                Houdini
                ${_houdini_hfs_root}/dsolib/libgusd.so
            )
        else ()
            target_link_libraries(${TARGET_NAME}
                Houdini			# Standard Houdini librarys
            )
        endif ()
    elseif (_houdini_platform_osx)
        # Link against Houdini libraries (including USD)
        set(_lib_dir "${_houdini_hfs_root}/Frameworks/Houdini.framework/Versions/Current/Libraries")
        target_link_libraries(${TARGET_NAME}
            Houdini
            ${_lib_dir}/libpxr_ar.dylib
            ${_lib_dir}/libpxr_arch.dylib
            ${_lib_dir}/libpxr_gf.dylib
            ${_lib_dir}/libpxr_js.dylib
            ${_lib_dir}/libpxr_kind.dylib
            ${_lib_dir}/libpxr_pcp.dylib
            ${_lib_dir}/libpxr_plug.dylib
            ${_lib_dir}/libpxr_sdf.dylib
            ${_lib_dir}/libpxr_tf.dylib
            ${_lib_dir}/libpxr_usd.dylib
            ${_lib_dir}/libpxr_usdGeom.dylib
            ${_lib_dir}/libpxr_usdRi.dylib
            ${_lib_dir}/libpxr_usdShade.dylib
            ${_lib_dir}/libpxr_usdUtils.dylib
            ${_lib_dir}/libpxr_vt.dylib
            ${_lib_dir}/libpxr_work.dylib
            ${_lib_dir}/libhboost_python${PYTHON_DOTLESS_VERSION}.dylib
            ${_lib_dir}/libtbb.dylib
            ${_houdini_hfs_root}/Frameworks/Python.framework/Versions/Current/lib/libpython${PYTHON_REQUESTED_VERSION}.dylib
        )
    elseif(_houdini_platform_win)
        # Link against Houdini libraries (including USD)
        target_link_libraries(${TARGET_NAME}
            Houdini
            ${_houdini_hfs_root}/custom/houdini/dsolib/libgusd.lib
            ${_houdini_hfs_root}/custom/houdini/dsolib/libpxr_ar.lib
            ${_houdini_hfs_root}/custom/houdini/dsolib/libpxr_arch.lib
            ${_houdini_hfs_root}/custom/houdini/dsolib/libpxr_gf.lib
            ${_houdini_hfs_root}/custom/houdini/dsolib/libpxr_js.lib
            ${_houdini_hfs_root}/custom/houdini/dsolib/libpxr_kind.lib
            ${_houdini_hfs_root}/custom/houdini/dsolib/libpxr_pcp.lib
            ${_houdini_hfs_root}/custom/houdini/dsolib/libpxr_plug.lib
            ${_houdini_hfs_root}/custom/houdini/dsolib/libpxr_sdf.lib
            ${_houdini_hfs_root}/custom/houdini/dsolib/libpxr_tf.lib
            ${_houdini_hfs_root}/custom/houdini/dsolib/libpxr_usd.lib
            ${_houdini_hfs_root}/custom/houdini/dsolib/libpxr_usdGeom.lib
            ${_houdini_hfs_root}/custom/houdini/dsolib/libpxr_usdRi.lib
            ${_houdini_hfs_root}/custom/houdini/dsolib/libpxr_usdShade.lib
            ${_houdini_hfs_root}/custom/houdini/dsolib/libpxr_usdUtils.lib
            ${_houdini_hfs_root}/custom/houdini/dsolib/libpxr_vt.lib
            ${_houdini_hfs_root}/custom/houdini/dsolib/libpxr_work.lib
            ${_houdini_hfs_root}/custom/houdini/dsolib/hboost_python${PYTHON_DOTLESS_VERSION}-mt-x64.lib
            ${_houdini_hfs_root}/python${PYTHON_DOTLESS_VERSION}/libs/python${PYTHON_DOTLESS_VERSION}.lib
            ${Boost_LIBRARIES}
            )
    endif()
    install (
        TARGETS ${TARGET_NAME} RUNTIME
        DESTINATION ${CMAKE_INSTALL_PREFIX}
    )
endfunction()


function(build_python_module PYTHON_REQUESTED_VERSION PROJECT_BUILD_TYPE)
    if (PYTHON_REQUESTED_VERSION VERSION_EQUAL 3.9)
        set(Python_ROOT_DIR "C:/Python39")
        set(BOOST_REQUESTED_VERSION 1.76.0)
        set(BOOST_ROOT "C:/local/boost_1_76_0")
    elseif (PYTHON_REQUESTED_VERSION VERSION_EQUAL 3.10)
        set(Python_ROOT_DIR "C:/Python310")
        set(BOOST_REQUESTED_VERSION 1.80.0)
        set(BOOST_ROOT "C:/local/boost_1_80_0")
    elseif (PYTHON_REQUESTED_VERSION VERSION_EQUAL 3.11)
        set(Python_ROOT_DIR "C:/Python311")
        set(BOOST_REQUESTED_VERSION 1.82.0)
        set(BOOST_ROOT "C:/local/boost_1_82_0")
    else ()
        message( FATAL_ERROR "Unsupported Python version: ${PYTHON_REQUESTED_VERSION}" )
    endif ()
    message (STATUS "Python version: ${PYTHON_REQUESTED_VERSION}")
    string (REPLACE "." "" PYTHON_DOTLESS_VERSION "${PYTHON_REQUESTED_VERSION}")
    set (CMAKE_BUILD_TYPE "${PROJECT_BUILD_TYPE}" CACHE INTERNAL "" FORCE)
    find_package (Python ${PYTHON_REQUESTED_VERSION} REQUIRED COMPONENTS Interpreter Development)
    find_package (Boost ${BOOST_REQUESTED_VERSION} EXACT REQUIRED COMPONENTS python${PYTHON_DOTLESS_VERSION} system filesystem)
    set (TARGET_NAME "${PROJECT_NAME}_python${PYTHON_DOTLESS_VERSION}")
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
