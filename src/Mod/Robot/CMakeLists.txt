
add_subdirectory(App)
if(FREECAD_BUILD_GUI)
    add_subdirectory(Gui)
endif(FREECAD_BUILD_GUI)

INSTALL(
    FILES
        Init.py
        InitGui.py
        KukaExporter.py
        MovieTool.py
        RobotExample.py
        RobotExampleTrajectoryOutOfShapes.py
    DESTINATION
        ${INSTALL_MOD_DIR}/Robot
)

INSTALL(
    DIRECTORY
        Lib
    DESTINATION
        ${CMAKE_INSTALL_DATADIR}/Mod/Robot
    PATTERN "Makefile*" EXCLUDE
    PATTERN "*.pdf" EXCLUDE
)

