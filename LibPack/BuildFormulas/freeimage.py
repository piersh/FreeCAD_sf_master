import libpack_utils as utils
import os

name = "freeimage"
version = "3.15.4"
source = {"type":"archive", "url":
          "http://downloads.sourceforge.net/freeimage/FreeImage3154.zip"}
depends_on = []
    
def build(libpack):
    utils.shutil.copy(os.path.join(os.path.dirname(__file__),
                      "..\\patches\\freeimage_CMakeLists.txt"),
                      "CMakeLists.txt")
    
    if not os.path.exists("cmake_build"):
        os.mkdir("cmake_build")
        
    os.chdir("cmake_build")
    
    tmp_install = os.path.join(libpack.config.get("Paths", "workspace"),
                               "tmp_install")
    
    if libpack.toolchain.startswith("vc"):
        if libpack.toolchain == "vc9":
            utils.run_cmd("cmake", ["-D","CMAKE_INSTALL_PREFIX=" + tmp_install,
                          "-G", "Visual Studio 9 2008", ".."])
            
            print("\nBuilding release...\n")
            utils.run_cmd("vcbuild", ["FreeImage.sln", "Release|Win32"])
            
            print("\nBuilding debug...\n")
            utils.run_cmd("vcbuild", ["FreeImage.sln", "Debug|Win32"])
        else:
            print(libpack.toolchain + " is not supported for " + name)
    
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

