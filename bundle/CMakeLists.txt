#install dependencies into app bundle -- must be done last
if(FREECAD_APP_BUNDLE)
        #directories to look for dependencies
        SET(DIRS ${FREECAD_LIBPACK}lib ${CMAKE_INSTALL_PREFIX}/${INSTALL_LIB_DIR})

        #location of app
        SET(APPS "\${CMAKE_INSTALL_PREFIX}/${BUNDLE_NAME}.app")

        configure_file(
            ${CMAKE_SOURCE_DIR}/cMake/InstallBundleDeps.cmake.in 
            ${CMAKE_BINARY_DIR}/InstallBundleDeps.cmake
            @ONLY
        )
        INSTALL(SCRIPT ${CMAKE_BINARY_DIR}/InstallBundleDeps.cmake)
endif(FREECAD_APP_BUNDLE)
