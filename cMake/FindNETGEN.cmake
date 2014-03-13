# Try to find nglib/netgen
# Once done this will define
#
# NGLIB_INCLUDE_DIR   - where the nglib include directory can be found
# NGLIB_LIBRARIES     - Link this to use nglib
# NETGEN_INCLUDE_DIRS - where the netgen include directories can be found
#
# See also: http://git.salome-platform.org/gitweb/?p=NETGENPLUGIN_SRC.git;a=summary

# nglib
FIND_PATH(NGLIB_INCLUDE_DIR nglib.h /usr/include)
FIND_LIBRARY(NGLIB_LIBRARIES nglib /usr/lib /usr/local/lib)

# netgen headers
SET(NETGEN_INCLUDE_DIRS)
SET(NETGEN_INCLUDE_DIRS ${NETGEN_INCLUDE_DIRS} -DNO_PARALLEL_THREADS -DOCCGEOMETRY)

SET(NETGENDATA /usr/share/netgen/libsrc)
FIND_PATH(NETGEN_DIR_csg csg.hpp HINTS ${NGLIB_INCLUDE_DIR}/netgen/csg PATHS ${NETGENDATA}/csg)
FIND_PATH(NETGEN_DIR_gen array.hpp HINTS ${NGLIB_INCLUDE_DIR}/netgen/general PATHS ${NETGENDATA}/general)
FIND_PATH(NETGEN_DIR_geom2d geom2dmesh.hpp HINTS ${NGLIB_INCLUDE_DIR}/netgen/geom2d PATHS ${NETGENDATA}/geom2d)
FIND_PATH(NETGEN_DIR_gprim gprim.hpp HINTS ${NGLIB_INCLUDE_DIR}/netgen/gprim PATHS ${NETGENDATA}/gprim)
FIND_PATH(NETGEN_DIR_la linalg.hpp HINTS ${NGLIB_INCLUDE_DIR}/netgen/linalg PATHS ${NETGENDATA}/linalg)
FIND_PATH(NETGEN_DIR_mesh meshing.hpp HINTS ${NGLIB_INCLUDE_DIR}/netgen/meshing PATHS ${NETGENDATA}/meshing)
FIND_PATH(NETGEN_DIR_occ occgeom.hpp HINTS ${NGLIB_INCLUDE_DIR}/netgen/occ PATHS ${NETGENDATA}/occ)
FIND_PATH(NETGEN_DIR_stlgeom stlgeom.hpp HINTS ${NGLIB_INCLUDE_DIR}/netgen/stlgeom PATHS ${NETGENDATA}/stlgeom)

SET(NETGEN_INCLUDE_DIRS ${NETGEN_INCLUDE_DIRS} ${NETGEN_DIR_csg})
SET(NETGEN_INCLUDE_DIRS ${NETGEN_INCLUDE_DIRS} ${NETGEN_DIR_gen})
SET(NETGEN_INCLUDE_DIRS ${NETGEN_INCLUDE_DIRS} ${NETGEN_DIR_geom2d})
SET(NETGEN_INCLUDE_DIRS ${NETGEN_INCLUDE_DIRS} ${NETGEN_DIR_gprim})
SET(NETGEN_INCLUDE_DIRS ${NETGEN_INCLUDE_DIRS} ${NETGEN_DIR_la})
SET(NETGEN_INCLUDE_DIRS ${NETGEN_INCLUDE_DIRS} ${NETGEN_DIR_mesh})
SET(NETGEN_INCLUDE_DIRS ${NETGEN_INCLUDE_DIRS} ${NETGEN_DIR_occ})
SET(NETGEN_INCLUDE_DIRS ${NETGEN_INCLUDE_DIRS} ${NETGEN_DIR_stlgeom})

