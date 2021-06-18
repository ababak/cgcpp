# (c) Andriy Babak 2020-2021
# 
# date: 08/09/2020
# modified: 18/06/2021 15:03:35
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


function(build_houdini_module HOUDINI_VERSION PROJECT_BUILD_TYPE)
    set (CMAKE_BUILD_TYPE "${PROJECT_BUILD_TYPE}" CACHE INTERNAL "" FORCE)
    set (TARGET_NAME "${PROJECT_NAME}")
    set (HFS "C:/sidefx/Houdini ${HOUDINI_VERSION}")
    find_package (Houdini REQUIRED)
    add_library (${TARGET_NAME} SHARED ${SRC})
    set_target_properties (${TARGET_NAME} PROPERTIES PREFIX "")
    target_compile_features(${TARGET_NAME} PUBLIC
        cxx_auto_type
        cxx_lambdas
        cxx_nullptr
        cxx_range_for
    )
    set(_houdini_python_version 2.7)
    set(_houdini_python_dotless_version 27)
    if (_houdini_platform_linux)
        # Link against Houdini libraries (including USD)
        if (DEFINED ENV{HOUDINI_HDK_LINK_GUSD})
        target_link_libraries(${PLUGIN_NAME}
            Houdini
            ${_houdini_hfs_root}/dsolib/libgusd.so
        )
        else ()
        target_link_libraries(${PLUGIN_NAME}
            Houdini			# Standard Houdini librarys
        )
        endif ()
    elseif (_houdini_platform_osx)
        # Link against Houdini libraries (including USD)
        set(_lib_dir "${_houdini_hfs_root}/Frameworks/Houdini.framework/Versions/Current/Libraries")
        target_link_libraries(${PLUGIN_NAME}
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
            ${_lib_dir}/libhboost_python${_houdini_python_dotless_version}.dylib
            ${_lib_dir}/libtbb.dylib
            ${_houdini_hfs_root}/Frameworks/Python.framework/Versions/Current/lib/libpython${_houdini_python_version}.dylib
        )
    elseif(_houdini_platform_win)
        # Link against Houdini libraries (including USD)
        target_link_libraries(${PLUGIN_NAME}
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
            ${_houdini_hfs_root}/custom/houdini/dsolib/hboost_python${_houdini_python_dotless_version}-mt-x64.lib
            ${_houdini_hfs_root}/python${_houdini_python_dotless_version}/libs/python${_houdini_python_dotless_version}.lib
        )
    endif()
    install (
        TARGETS ${TARGET_NAME} RUNTIME
        DESTINATION ${CMAKE_INSTALL_PREFIX}
    )
endfunction()



function(build_python_module PROJECT_BUILD_TYPE)
    set (CMAKE_BUILD_TYPE "${PROJECT_BUILD_TYPE}" CACHE INTERNAL "" FORCE)
    set (HFS "${PROJECT_BUILD_TYPE}" CACHE INTERNAL "" FORCE)
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
