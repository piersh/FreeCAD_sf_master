import libpack_utils as utils
import os
from subprocess import CalledProcessError

name = "python"
version = "2.7.6"
source = {"type":"archive", "url":
          "http://www.python.org/ftp/python/2.7.6/Python-2.7.6.tgz"}
depends_on = []
    
def build(libpack):
    
    if libpack.toolchain.startswith("vc"):
        utils.apply_patch(os.path.join(os.path.dirname(__file__),
                          "..\\patches\\python_pyconfig.diff"))
        
        if libpack.toolchain == "vc9":
            try:
                print("\nBuilding release...\n")
                utils.run_cmd("vcbuild", ["PCbuild\\pcbuild.sln",
                                          "Release|Win32"])
                print("\nBuilding debug...\n")
                utils.run_cmd("vcbuild", ["PCbuild\\pcbuild.sln",
                                          "Debug|Win32"])
            except CalledProcessError as e:
                #ignore errors because we don't need the modules that
                #fail to build
                print(e)
            

    
def install(libpack): 
    files = utils.copytree("Include", libpack.path, "include\\python2.7")
    files.extend(utils.copyfiles(["PC\\pyconfig.h"], libpack.path, "include\\python2.7"))
    
    utils.run_cmd("7z", ["a", "-r", libpack.path + "\\bin\\python27.zip", ".\\Lib\\*"],
                  silent=True)
    files.append("bin\\python27.zip")
    
    files.extend(utils.copyfiles(["PCbuild\\python27.lib", "PCbuild\\python27_d.lib"],
                                 libpack.path, "lib"))
    
    files.extend(utils.copyfiles(["PCbuild\\python.exe", "PCbuild\\python_d.exe",
                                  "PCbuild\\*.dll", "PCbuild\\*.pyd"], libpack.path, "bin"))
    
    libpack.manifest_add(name, version, files)

