# Locate Xerces-C include paths and libraries
# Xerces-C can be found at http://xml.apache.org/xerces-c/
# Written by Frederic Heem, frederic.heem _at_ telsey.it
# Modified by Jos van den Oever

# This module defines
# XERCESC_INCLUDE_DIR, where to find ptlib.h, etc.
# XERCESC_LIBRARIES, the libraries to link against to use pwlib.
# XERCESC_FOUND, If false, don't try to use pwlib.

FIND_PATH(XERCESC_INCLUDE_DIR xercesc/dom/DOM.hpp
  "[HKEY_CURRENT_USER\\software\\xerces-c\\src]"
  "[HKEY_CURRENT_USER\\xerces-c\\src]"
  $ENV{XERCESCROOT}/include/
  $ENV{XERCESCROOT}/src/
  /usr/local/include
  /usr/include
)

IF(NOT LIB_DESTINATION)
    SET(${LIB_DESTINATION} lib)
ENDIF(NOT LIB_DESTINATION)

IF(WIN32)
	FIND_LIBRARY(XERCESC_LIBRARY_RELEASE
	  NAMES
		xerces-c xerces-c_2 xerces-c_3
	  PATHS
		"[HKEY_CURRENT_USER\\software\\xerces-c\\lib]"
		"[HKEY_CURRENT_USER\\xerces-c\\lib]"
		$ENV{XERCESCROOT}/${LIB_DESTINATION}
	)
	FIND_LIBRARY(XERCESC_LIBRARY_DEBUG
	  NAMES
		xerces-cD xerces-c_2D xerces-c_3D
	  PATHS
		"[HKEY_CURRENT_USER\\software\\xerces-c\\lib]"
		"[HKEY_CURRENT_USER\\xerces-c\\lib]"
		$ENV{XERCESCROOT}/${LIB_DESTINATION}
	)
	
	include(SelectLibraryConfigurations)
    SELECT_LIBRARY_CONFIGURATIONS(XERCESC)
ELSE(WIN32)
	FIND_LIBRARY(XERCESC_LIBRARY
	  NAMES
		xerces-c
	  PATHS
		$ENV{XERCESCROOT}/${LIB_DESTINATION}
		/usr/local/${LIB_DESTINATION}
		/usr/${LIB_DESTINATION}
	)
	SET(SOQT_LIBRARIES ${SOQT_LIBRARY})
ENDIF(WIN32)

include(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(XercesC REQUIRED_VARS XERCESC_LIBRARIES XERCESC_INCLUDE_DIR)

#MARK_AS_ADVANCED(
#  XERCESC_INCLUDE_DIR
#  XERCESC_LIBRARIES
#)
