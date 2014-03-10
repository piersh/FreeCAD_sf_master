import libpack_utils as utils
import os

name = "zlib"
version = "1.2.8"
source = {"type":"archive", "url":"http://zlib.net/zlib128.zip"}
depends_on = []
    
def build(libpack):
    if not os.path.exists("cmake_build"):
        os.mkdir("cmake_build")
        
    os.chdir("cmake_build")
    
    tmp_install = os.path.join(libpack.config.get("Paths", "workspace"),
                               "tmp_install")
    
    generator = ""
    
    if libpack.toolchain.startswith("vc"):
        if libpack.toolchain == "vc9":
            generator = "Visual Studio 9 2008"
        else:
            print(libpack.toolchain + " not supported for " + name)
        
        utils.run_cmd("cmake", ["-D", "CMAKE_INSTALL_PREFIX=" + tmp_install,
                                "-G", generator, ".."])

        print("\nBuilding debug...\n")
        utils.run_cmd("vcbuild", ["zlib.sln", "Debug|Win32"])
        
        print("\nBuilding release...\n")
        utils.run_cmd("vcbuild", ["zlib.sln", "Release|Win32"])
    
def install(libpack):
    tmp_install = os.path.join(libpack.config.get("Paths", "workspace"),
                               "tmp_install")
    
    if libpack.toolchain.startswith("vc"):
        if libpack.toolchain == "vc9":
            utils.run_cmd("vcbuild", ["INSTALL.vcproj", "Debug|Win32"])
            utils.run_cmd("vcbuild", ["INSTALL.vcproj", "Release|Win32"])
                    
    files = utils.move(tmp_install + "\\include", libpack.path, "include",
                       root=False)
    
    files.extend(utils.move(tmp_install + "\\lib", libpack.path, "lib",
                            root=False))
    files.extend(utils.move(tmp_install + "\\bin", libpack.path, "bin",
                            root=False))
    
    libpack.manifest_add(name, version, files)

    os.chdir("..")
    utils.shutil.rmtree(tmp_install)

