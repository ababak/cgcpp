#
# Simple module to find USD.
#
# Expected input variables:
# - USD_INSTALL_ROOT
# - USD_INCLUDES_DIR (default ${USD_INSTALL_ROOT}/include)
# - USD_LIBRARIES_DIR (default ${USD_INSTALL_ROOT}/lib)
# - USD_GENSCHEMA_DIR (default ${USD_INSTALL_ROOT}/bin)
# - USD_LIB_PREFIX: dcc specific prefix for component library
#
# Return variables:
# - USD_INCLUDE_DIR
# - USD_LIBRARY_DIR
# - USD_LIBRARIES
# - USD_GENSCHEMA
# - USD_VERSION
unset (USD_INCLUDE_DIR CACHE)
unset (USD_LIBRARY_DIR CACHE)
unset (USD_LIBRARIES CACHE)
unset (USD_GENSCHEMA CACHE)
unset (USD_VERSION CACHE)

if (NOT USD_FIND_COMPONENTS)
    message ("* USD_FIND_COMPONENTS is empty. Set it to default.")
    set (USD_FIND_COMPONENTS
        # usd
        ar
        arch
        js
        tf 
        vt 
    )
endif ()

if (EXISTS "$ENV{USD_INSTALL_ROOT}")
    set (USD_INSTALL_ROOT $ENV{USD_INSTALL_ROOT})
endif ()

find_path (USD_INCLUDE_DIR 
        pxr/pxr.h
        PATHS ${USD_INSTALL_ROOT}/include ${USD_INCLUDES_DIR}
        DOC "USD Include directory")

if (LINUX)
    set (libusd_name ${USD_LIB_PREFIX}usd.so) 
elseif (WIN32)
    set (libusd_name ${USD_LIB_PREFIX}usd.lib)
elseif (APPLE)
    set (libusd_name ${USD_LIB_PREFIX}usd.dylib)
endif ()

find_path (USD_LIBRARY_DIR 
        ${libusd_name}
        PATHS ${USD_INSTALL_ROOT}/lib ${USD_LIBRARIES_DIR}
        DOC "USD Libraries directory")

if (USD_LIBRARY_DIR)
    if (LINUX)
        set (LIBRARY_SUFFIX ".so")
    elseif (WIN32)
        set (LIBRARY_SUFFIX ".lib")
    elseif (APPLE)
        set (LIBRARY_SUFFIX ".dylib")
    endif ()
    message ("* USD_LIBRARY_DIR = ${USD_LIBRARY_DIR}")
    foreach (_lib ${USD_FIND_COMPONENTS})
        set (lib_name "${USD_LIBRARY_DIR}/${USD_LIB_PREFIX}${_lib}${LIBRARY_SUFFIX}")
        # message (${lib_name})
        if (EXISTS ${lib_name})
            message (STATUS "found ${_lib}")
            list (APPEND USD_LIBRARIES ${USD_LIB_PREFIX}${_lib}${LIBRARY_SUFFIX})
        else ()
            message (SEND_ERROR "${_lib} not found")
        endif ()
    endforeach ()
    message ("* USD_LIBRARIES = ${USD_LIBRARIES}")
endif ()

find_file (USD_GENSCHEMA
        names usdGenSchema
        PATHS ${USD_INSTALL_ROOT}/bin ${USD_GENSCHEMA_DIR}
        DOC "USD Gen schema application")

if (USD_INCLUDE_DIR AND EXISTS "${USD_INCLUDE_DIR}/pxr/pxr.h")
    foreach (_usd_comp MAJOR MINOR PATCH)
        file (STRINGS
             "${USD_INCLUDE_DIR}/pxr/pxr.h"
             _usd_tmp
             REGEX "#define PXR_${_usd_comp}_VERSION .*$")
        string (REGEX MATCHALL "[0-9]+" USD_${_usd_comp}_VERSION ${_usd_tmp})
    endforeach ()
    set (USD_VERSION ${USD_MAJOR_VERSION}.${USD_MINOR_VERSION}.${USD_PATCH_VERSION})
endif ()

include (FindPackageHandleStandardArgs)

find_package_handle_standard_args (USD
    REQUIRED_VARS
        USD_INCLUDE_DIR
        USD_LIBRARY_DIR
        USD_LIBRARIES
        USD_GENSCHEMA
    VERSION_VAR
        USD_VERSION
)
