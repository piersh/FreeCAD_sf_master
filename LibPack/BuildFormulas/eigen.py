import libpack_utils as utils
import os

name = "eigen"
version = "3.2.1"
source = {"type":"archive", "url":
          "http://bitbucket.org/eigen/eigen/get/3.2.1.zip"}
depends_on = []
    
def build(libpack):
    if not os.path.exists("cmake_build"):
        os.mkdir("cmake_build")
        
    os.chdir("cmake_build")

    generator = ""
    
    if libpack.toolchain.startswith("vc"):
        if libpack.toolchain == "vc9":
            generator = "Visual Studio 9 2008"
        
        utils.run_cmd("cmake", ["-D", "CMAKE_INSTALL_PREFIX=" + libpack.path,
                                "-G", generator, ".."])
    
def install(libpack):
    if libpack.toolchain.startswith("vc"):
        utils.run_cmd("vcbuild", ["INSTALL.vcproj", "Release|Win32"])
            
    files = ["include\\eigen3"]

    libpack.manifest_add(name, version, files)

    os.chdir("..")


