import libpack_utils as utils
import os
from sys import platform

name = "qt"
version = "4.8.5"
source = {"type":"archive", "url":
          "http://download.qt-project.org/official_releases"\
          "/qt/4.8/4.8.5/qt-everywhere-opensource-src-4.8.5.zip"}
depends_on = []
    
def build(libpack):
    tmp_install = os.path.join(libpack.config.get("Paths", "workspace"),
                               "tmp_install")
    
    if platform == "win32":
        print("\nBuilding release and debug...\n")
        utils.run_shell("configure -opensource -confirm-license "
                        "-debug-and-release -mp -no-qt3support "
                        "-no-phonon -no-multimedia -no-declarative-debug "
                        "-nomake tests -nomake examples -nomake demos "
                        "-nomake docs -no-vcproj")
        utils.run_cmd("nmake")

    
def install(libpack):
    if platform == "win32":  
        files = utils.copytree("include", libpack.path, "include", root=False,
                               ignore=utils.ignore_names("phonon",
                                                         "phonon_compat",
                                                         "Qt3Support",
                                                         "QtOpenVG",
                                                         "QtMultimedia",
                                                         "private", "*.pri"))
    
        files.extend(utils.copytree("lib", libpack.path, "lib", root=False,
                                    ignore=utils.ignore_names_inverse(["*.lib"])))
        files.extend(utils.copytree("bin", libpack.path, "bin", root=False,
                                    ignore=utils.ignore_names_inverse(["*.dll",
                                                                       "*.exe"])))
        files.extend(utils.copytree("plugins", libpack.path, "bin\\qtplugins",
                                    ignore=utils.ignore_names_inverse(
                                        ["*.dll"],
                                        ["bearer",
                                         "designer",
                                         "graphicssystems",
                                         "qmltooling"]
                                    )))

        libpack.manifest_add(name, version, files)
