#install dependencies into app bundle -- must be done last
if(FREECAD_APP_BUNDLE)
        #directories to look for dependencies
        SET(BUNDLE_DEPS_DIRS "/usr/local/lib" CACHE STRING 
            "Directories that fixup_bundle will search for libs")
        SET(DIRS ${BUNDLE_DEPS_DIRS} 
            ${CMAKE_INSTALL_PREFIX}/${INSTALL_LIB_DIR}
            #PartDesign is special
            ${CMAKE_INSTALL_PREFIX}/${INSTALL_MOD_DIR}/PartDesign
        )

        #location of app
        SET(APPS "\${CMAKE_INSTALL_PREFIX}/${BUNDLE_NAME}.app")

        # Install needed Qt plugins by copying directories from the qt installation
        INSTALL(DIRECTORY "${QT_PLUGINS_DIR}/imageformats" DESTINATION ${INSTALL_LIB_DIR}/plugins)

        configure_file(
            ${CMAKE_SOURCE_DIR}/cMake/InstallBundleDeps.cmake.in 
            ${CMAKE_BINARY_DIR}/InstallBundleDeps.cmake
            @ONLY
        )
        INSTALL(SCRIPT ${CMAKE_BINARY_DIR}/InstallBundleDeps.cmake)
        INSTALL(FILES qt.conf DESTINATION ${INSTALL_EXE_DIR}/../Resources)
endif(FREECAD_APP_BUNDLE)
