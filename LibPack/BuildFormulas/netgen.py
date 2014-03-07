import libpack_utils as utils
import os
from subprocess import CalledProcessError

name = "netgen"
version = "4.9.13"
source = {"type":"archive", "url":
          "http://sourceforge.net/projects/netgen-mesher/files/netgen-mesher"\
          "/4.9.13/netgen-4.9.13.zip"}
depends_on = ["oce"]
    
def build(libpack):
    
    if libpack.toolchain.startswith("vc"):
        if libpack.toolchain == "vc9":
            #for now, use netgen's pre-compiled dependencies
            if not os.path.exists("..\\ext_libs"):
                os.mkdir("..\\ext_libs")
            bit = "32"
            if libpack.arch == "x64": bit = "64"
            
            pthread_url = "http://sourceforge.net/projects/netgen-mesher/files"\
                          "/netgen-mesher/Additional%20Files/MSVC2008_Libs"\
                          "/pthread-w" + bit + ".zip"
            #tcl_url = "http://sourceforge.net/projects/netgen-mesher/files"\
            #          "/netgen-mesher/Additional%20Files/MSVC2008_Libs"\
            #          "/TclTkTixTogl-w" + bit + ".zip"
            utils.get_source({"type":"archive", "url":pthread_url},
                              "..\\ext_libs")

            utils.apply_patch(os.path.join(os.path.dirname(__file__),
                              "..\\patches\\netgen_vcproj.diff"))
            utils.apply_patch(os.path.join(os.path.dirname(__file__),
                              "..\\patches\\netgen_occ67_1.diff"))
            utils.apply_patch(os.path.join(os.path.dirname(__file__),
                              "..\\patches\\netgen_occ67_2.diff"))
            utils.apply_patch(os.path.join(os.path.dirname(__file__),
                              "..\\patches\\netgen_occ67_3.diff"))
            utils.apply_patch(os.path.join(os.path.dirname(__file__),
                              "..\\patches\\netgen_occ67_4.diff"))

            os.environ["LIB"] = os.environ["LIB"] + libpack.path + "\\lib"
            os.environ["INCLUDE"] = os.environ["INCLUDE"] + libpack.path \
                                    + "\\include\\oce"

            print("\nBuilding release...\n")
            utils.run_cmd("vcbuild", ["/useenv", "windows\\nglib.sln",
                                      "Release(OCC)|Win32"])
            print("\nBuilding debug...\n")
            utils.run_cmd("vcbuild", ["/useenv", "windows\\nglib.sln",
                                      "Debug|Win32"])

def install(libpack):
    files = utils.copyfiles(["nglib\\nglib.h"], libpack.path, "include")
    
    files.extend(utils.copyfiles(["windows\\nglib\\Debug\\*.lib",
                                  "windows\\nglib\\Release(OCC)\\*.lib"],
                                 libpack.path, "lib"))
    
    files.extend(utils.copyfiles(["windows\\nglib\\Debug\\*.dll",
                                  "windows\\nglib\\Release(OCC)\\*.dll"],
                                 libpack.path, "bin"))

    libpack.manifest_add(name, version, files)

