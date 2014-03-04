import libpack_utils as utils
import os

name = "freetype"
version = "2.5.2"
source = {"type":"archive", "url":
          "http://sourceforge.net/projects/freetype/files/freetype2/2.5.2/ft252.zip"}
depends_on = []
    
def build(libpack):
    utils.shutil.copy(os.path.join(os.path.dirname(__file__),
                      "..\\patches\\freetype_CMakeLists.txt"),
                      "CMakeLists.txt")
    
    if not os.path.exists("cmake_build"):
        os.mkdir("cmake_build")

    os.chdir("cmake_build")
    
    tmp_install = os.path.join(libpack.config.get("Paths", "workspace"),
                               "tmp_install")

    generator = ""
    
    if libpack.toolchain.startswith("vc"):
        utils.apply_patch(os.path.join(os.path.dirname(__file__),
                              "..\\patches\\freetype_dll_export.diff"),
                          "..")
        if libpack.toolchain == "vc9":
            generator = "Visual Studio 9 2008"
        else:
            print(libpack.toolchain + " not supported for " + name)

            
        utils.run_cmd("cmake", ["-D", "CMAKE_INSTALL_PREFIX=" + tmp_install, 
                                "-G", generator, ".."])
            
        print("\nBuilding release...\n")
        utils.run_cmd("vcbuild", ["freetype.sln", "Release|Win32"])

        print("\nBuilding debug...\n")
        utils.run_cmd("vcbuild", ["freetype.sln", "Debug|Win32"])
    
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

