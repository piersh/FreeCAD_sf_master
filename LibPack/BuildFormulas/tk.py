import libpack_utils as utils
import os

name = "tk"
version = "8.6.1"
source = {
    "type":"archive",
    "url": "http://prdownloads.sourceforge.net/tcl/tk{0}-src.tar.gz".format(version)
}
depends_on = ["tcl"]
patches = []

def build(libpack):

    if libpack.toolchain.startswith("vc"):

        old_dir = os.getcwd()
        os.chdir("win")

        os.environ["TCLDIR"] = libpack.get_formula_dir("tcl")

        utils.run_cmd("nmake", ["/f", "makefile.vc"])

        os.chdir(old_dir)


def install(libpack):

    tmp_install = os.path.join(libpack.config.get("Paths", "workspace"),
                               "tmp_install")

    if libpack.toolchain.startswith("vc"):
        old_dir = os.getcwd()
        os.chdir("win")

        utils.run_cmd("nmake", ["/f", "makefile.vc",
                                "INSTALLDIR={0}".format(tmp_install),
                                "install" ])

        os.chdir(old_dir)

    old_dir = os.getcwd()
    os.chdir(tmp_install)

    files = utils.copytree("bin", libpack.path, "bin", root=False)
    files.extend(utils.copytree("lib", libpack.path, "lib", root=False))
    files.extend(utils.copytree("include", libpack.path, "include", root=False))

    os.chdir(old_dir)

    print(os.getcwd())

    # install-private-headers would have been nice...
    files.extend(utils.copyfiles(["generic\\tklInt.h",
                                  "generic\\tkIntDecls.h",
                                  "generic\\tkIntPlatDecls.h",
                                  "generic\\tkPort.h",
                                  "win\\tkWinPort.h",
                                  "win\\tkWinInt.h",
                                  "win\\tkWin.h"],
                                 libpack.path, "include"));

    libpack.manifest_add(name, version, files)
