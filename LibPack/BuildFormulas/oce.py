import libpack_utils as utils
import os

name = "oce"
version = "3.15.4"
source = {"type":"archive", "url":
          "https://github.com/tpaviot/oce/archive/OCE-0.15.zip"}
depends_on = ["freetype", "freeimage"]
    
def build(libpack):
    if not os.path.exists("cmake_build"):
        os.mkdir("cmake_build")
        
    os.chdir("cmake_build")
    
    tmp_install = os.path.join(libpack.config.get("Paths", "workspace"),
                               "tmp_install")

    os.environ["CMAKE_PREFIX_PATH"] = libpack.path
    #os.environ["FREETYPE_DIR"] = libpack.path

    generator = ""
    
    if libpack.toolchain.startswith("vc"):
        if libpack.toolchain == "vc9":
            generator = "Visual Studio 9 2008"
        else:
            print(libpack.toolchain + " not supported for " + name)

        ft_include = "FREETYPE_INCLUDE_DIRS="\
                 "{0}/include/freetype2".format(libpack.path)
        
        utils.run_cmd("cmake", ["-D", "OCE_INSTALL_PREFIX=" + tmp_install,
                                "-D", "OCE_INSTALL_BIN_DIR=bin",
                                "-D", "OCE_INSTALL_LIB_DIR=lib",
                                #"-D", "OCE_INSTALL_PACKAGE_LIB_DIR=lib",
                                #"-D", "OCE_INSTALL_PDB_FILES=OFF",
                                #"-D", "OCE_MULTITHREADED_BUILD=OFF",
                                "-D", ft_include,
                                "-D", "OCE_USE_MSVC_EXPRESS=ON",
                                "-D", "OCE_DRAW=ON",
                                "-D", "OCE_WITH_FREEIMAGE=ON",
                                "-D", "CMAKE_USE_RELATIVE_PATHS=ON",
                                "-G", generator, ".."])
            
        print("\nBuilding release...\n")
        utils.run_cmd("vcbuild", ["OCE.sln", "Release|Win32"])

        print("\nBuilding debug...\n")
        utils.run_cmd("vcbuild", ["OCE.sln", "Debug|Win32"])
    
def install(libpack):
    tmp_install = os.path.join(libpack.config.get("Paths", "workspace"),
                               "tmp_install")
    
    if libpack.toolchain.startswith("vc"):
        if libpack.toolchain == "vc9":
            utils.run_cmd("vcbuild", ["INSTALL.vcproj", "Release|Win32"])
            utils.run_cmd("vcbuild", ["INSTALL.vcproj", "Debug|Win32"])
            
    files = utils.move(os.path.join(tmp_install, "include"),
                       libpack.path, "include", root=False)
    
    files.extend(utils.move(os.path.join(tmp_install, "lib"),
                            libpack.path, "lib", root=False))
    files.extend(utils.move(os.path.join(tmp_install, "bin"),
                            libpack.path, "bin", root=False))

    libpack.manifest_add(name, version, files)

    os.chdir("..")
    utils.shutil.rmtree(tmp_install)

