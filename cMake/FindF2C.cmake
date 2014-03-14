# This module finds f2c.
#
# This module sets the following variables:
#  F2C_FOUND - set to true if library is found
#  F2C_INCLUDE_DIR - path to f2c.h
#  F2C_LIBRARY - f2c library name (using full path name)
#  F2C_EXECUTABLE - the f2c executable (using full path name)

find_path(F2C_INCLUDE_DIR f2c.h)

find_library(F2C_LIBRARY NAMES f2c vcf2c)

find_program(F2C_EXECUTABLE f2c)

include(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(F2C REQUIRED_VARS 
    F2C_INCLUDE_DIR 
    F2C_LIBRARY
    F2C_EXECUTABLE)
