#add_defintions(-D_FC_GUI_ENABLED_)
#add_defintions(-DFREECADMAINPY)

if(FREECAD_BUILD_GUI)
    include_directories(
        ${Boost_INCLUDE_DIRS}
        ${COIN3D_INCLUDE_DIR}
        ${ZLIB_INCLUDE_DIR}
        ${SOQT_INCLUDE_DIR}
        ${QT_INCLUDE_DIR}
        ${PYTHON_INCLUDE_PATH}
        ${XERCESC_INCLUDE_DIR}
    )
else(FREECAD_BUILD_GUI)
    include_directories(
        ${Boost_INCLUDE_DIRS}
        ${ZLIB_INCLUDE_DIR}
        ${QT_INCLUDE_DIR}
        ${PYTHON_INCLUDE_PATH}
        ${XERCESC_INCLUDE_DIR}
    )
endif(FREECAD_BUILD_GUI)

######################## FreeCADMain ########################
if(FREECAD_BUILD_GUI)

    SET(FreeCAD_SRCS
        freecad.rc
        icon.ico
        MainGui.cpp
    )

    if(FREECAD_APP_BUNDLE)
        set_source_files_properties(freecad.icns PROPERTIES MACOSX_PACKAGE_LOCATION Resources)
        SET(FreeCAD_SRCS ${FreeCAD_SRCS} freecad.icns)
    endif(FREECAD_APP_BUNDLE)

    if(MSVC)
        SET(FreeCAD_LIBS
            FreeCADGui
            debug qtmaind.lib
            optimized qtmain.lib
        )
    else(MSVC)
        SET(FreeCAD_LIBS
            FreeCADGui
        )
    endif(MSVC)

    add_executable(FreeCADMain WIN32 ${FreeCAD_SRCS})

    target_link_libraries(FreeCADMain ${FreeCAD_LIBS})

    # Note this is IDE specific, not necessarily platform specific
    if(MSVC)
        set_target_properties(FreeCADMain PROPERTIES OUTPUT_NAME "FreeCAD")
        set_target_properties(FreeCADMain PROPERTIES DEBUG_OUTPUT_NAME "FreeCADD")
        # dirty hack to avoid Debug/Release subdirectory
        set_target_properties(FreeCADMain PROPERTIES PREFIX "../")
        set_target_properties(FreeCADMain PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
    elseif(MINGW)
        set_target_properties(FreeCADMain PROPERTIES OUTPUT_NAME "FreeCAD")
        set_target_properties(FreeCADMain PROPERTIES DEBUG_OUTPUT_NAME "FreeCADD")
        set_target_properties(FreeCADMain PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
    else(MSVC)
        set_target_properties(FreeCADMain PROPERTIES OUTPUT_NAME "FreeCAD")
        set_target_properties(FreeCADMain PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
        set_target_properties(FreeCADMain PROPERTIES INSTALL_RPATH ${INSTALL_RPATH})
    endif(MSVC)

    #Application bundle settings
    if(FREECAD_APP_BUNDLE)
        set_target_properties(FreeCADMain PROPERTIES MACOSX_BUNDLE TRUE)
        SET(MACOSX_BUNDLE_BUNDLE_NAME ${BUNDLE_NAME})
        SET(MACOSX_BUNDLE_ICON_FILE freecad.icns)
    endif(FREECAD_APP_BUNDLE)

    if(WIN32)
        INSTALL(TARGETS FreeCADMain
            RUNTIME DESTINATION bin
            LIBRARY DESTINATION lib
        )
    else(WIN32)
        #Install bundle at root of install tree. If no bundle, executable will be in bin as usual.
        INSTALL(TARGETS FreeCADMain 
            BUNDLE DESTINATION .
            RUNTIME DESTINATION bin
        )
    endif(WIN32)
endif(FREECAD_BUILD_GUI)
######################## FreeCADMainCmd ########################

SET(FreeCADMainCmd_SRCS
    MainCmd.cpp
)
add_executable(FreeCADMainCmd ${FreeCADMainCmd_SRCS})

target_link_libraries(FreeCADMainCmd 
    FreeCADApp
    ${QT_DEBUG_LIBRARIES}
    ${QT_LIBRARIES}
)

# Note this is IDE specific, not necessarily platform specific
if(MSVC)
    set_target_properties(FreeCADMainCmd PROPERTIES OUTPUT_NAME "FreeCADCmd")
    set_target_properties(FreeCADMainCmd PROPERTIES DEBUG_OUTPUT_NAME "FreeCADCmdD")
    # dirty hack to avoid Debug/Release subdirectory
    set_target_properties(FreeCADMainCmd PROPERTIES PREFIX "../")
    set_target_properties(FreeCADMainCmd PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
elseif(MINGW)
    set_target_properties(FreeCADMainCmd PROPERTIES OUTPUT_NAME "FreeCADCmd")
    set_target_properties(FreeCADMainCmd PROPERTIES DEBUG_OUTPUT_NAME "FreeCADCmdD")
    set_target_properties(FreeCADMainCmd PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
else(MSVC)
    set_target_properties(FreeCADMainCmd PROPERTIES OUTPUT_NAME "FreeCADCmd")
    set_target_properties(FreeCADMainCmd PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
    set_target_properties(FreeCADMainCmd PROPERTIES INSTALL_RPATH ${INSTALL_RPATH})
endif(MSVC)

if(WIN32)
    INSTALL(TARGETS FreeCADMainCmd
        RUNTIME DESTINATION bin
        LIBRARY DESTINATION lib
    )
else(WIN32)
    INSTALL(TARGETS FreeCADMainCmd 
        RUNTIME DESTINATION ${INSTALL_EXE_DIR}
    )
endif(WIN32)

######################## FreeCADMainPy ########################

SET(FreeCADMainPy_SRCS
     MainPy.cpp
)

add_library(FreeCADMainPy SHARED ${FreeCADMainPy_SRCS})

target_link_libraries(FreeCADMainPy FreeCADApp)

# Note this is IDE specific, not necessarily platform specific
if(MSVC)
    set_target_properties(FreeCADMainPy PROPERTIES OUTPUT_NAME "FreeCAD")
    set_target_properties(FreeCADMainPy PROPERTIES DEBUG_OUTPUT_NAME "FreeCAD_d")
    set_target_properties(FreeCADMainPy PROPERTIES SUFFIX ".pyd")
    # dirty hack to avoid Debug/Release subdirectory
    set_target_properties(FreeCADMainPy PROPERTIES PREFIX "../")
    set_target_properties(FreeCADMainPy PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
elseif(MINGW)
    set_target_properties(FreeCADMainPy PROPERTIES OUTPUT_NAME "FreeCAD")
    set_target_properties(FreeCADMainPy PROPERTIES DEBUG_OUTPUT_NAME "FreeCAD_d")
    set_target_properties(FreeCADMainPy PROPERTIES SUFFIX ".pyd")
    set_target_properties(FreeCADMainPy PROPERTIES PREFIX "")
    set_target_properties(FreeCADMainPy PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
else(MSVC)
    set_target_properties(FreeCADMainPy PROPERTIES OUTPUT_NAME "FreeCAD")
    set_target_properties(FreeCADMainPy PROPERTIES PREFIX "")
    set_target_properties(FreeCADMainPy PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
    set_target_properties(FreeCADMainPy PROPERTIES INSTALL_RPATH ${INSTALL_RPATH})
endif(MSVC)

if(WIN32)
    INSTALL(TARGETS FreeCADMainPy
        RUNTIME DESTINATION bin
        LIBRARY DESTINATION lib
    )
else(WIN32)
    INSTALL(TARGETS FreeCADMainPy
        LIBRARY DESTINATION ${INSTALL_LIB_DIR}
    )
endif(WIN32)

######################## FreeCADGuiPy ########################
if(FREECAD_BUILD_GUI)

    SET(FreeCADGuiPy_SRCS
        FreeCADGuiPy.cpp
    )

    add_library(FreeCADGuiPy SHARED ${FreeCADGuiPy_SRCS})

    target_link_libraries(FreeCADGuiPy FreeCADGui)

    # Note this is IDE specific, not necessarily platform specific
    if(MSVC)
        set_target_properties(FreeCADGuiPy PROPERTIES OUTPUT_NAME "FreeCADGui")
        set_target_properties(FreeCADGuiPy PROPERTIES DEBUG_OUTPUT_NAME "FreeCADGui_d")
        set_target_properties(FreeCADGuiPy PROPERTIES SUFFIX ".pyd")
        # dirty hack to avoid Debug/Release subdirectory
        set_target_properties(FreeCADGuiPy PROPERTIES PREFIX "../")
        set_target_properties(FreeCADGuiPy PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
    elseif(MINGW)
        set_target_properties(FreeCADGuiPy PROPERTIES OUTPUT_NAME "FreeCADGui")
        set_target_properties(FreeCADGuiPy PROPERTIES DEBUG_OUTPUT_NAME "FreeCADGui_d")
        set_target_properties(FreeCADGuiPy PROPERTIES SUFFIX ".pyd")
        set_target_properties(FreeCADGuiPy PROPERTIES PREFIX "")
        set_target_properties(FreeCADGuiPy PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
    else(MSVC)
        set_target_properties(FreeCADGuiPy PROPERTIES OUTPUT_NAME "FreeCADGui")
        set_target_properties(FreeCADGuiPy PROPERTIES PREFIX "")
        set_target_properties(FreeCADGuiPy PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
        set_target_properties(FreeCADGuiPy PROPERTIES INSTALL_RPATH ${INSTALL_RPATH})
    endif(MSVC)

    if(WIN32)
        INSTALL(TARGETS FreeCADGuiPy
            RUNTIME DESTINATION bin
            LIBRARY DESTINATION lib
        )
    else(WIN32)
        INSTALL(TARGETS FreeCADGuiPy
            LIBRARY DESTINATION ${INSTALL_LIB_DIR}
        )
    endif(WIN32)

endif(FREECAD_BUILD_GUI)
