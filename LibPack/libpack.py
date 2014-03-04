from __future__ import print_function
import sys
import os
import shutil
import optparse
import pkgutil
import sqlite3
from ConfigParser import SafeConfigParser
from subprocess import CalledProcessError

import libpack_utils as utils

LIBPACK = None

class LibPackError(Exception):
    pass

class LibPack:
    """
    Create and maintain a set of compiled libraries
    """
    def __init__(self, config_path=None):
        self.config = SafeConfigParser()
        self.exists = False
        self.path = None
        self.toolchain = None
        self.arch = None
        
        self._build_formulas = {}
        self._config_file_path = None
        self._manifest_path = None
        
        self._load_config(config_path)

        if not os.path.exists(self.config.get("Paths", "root_dir")):
            os.mkdir(self.config.get("Paths", "root_dir"))
        if not os.path.exists(self.config.get("Paths", "workspace")):
            os.mkdir(self.config.get("Paths", "workspace"))
        self.write_config_file()
        
    def _load_config(self, path):
        default_dir = os.path.join(os.path.expanduser('~'), "FClib_pkg")
        if path == None:
            path = os.path.join(default_dir, "FCLib_pkg.cfg")
        if os.path.exists(path):
            with open(path, "r") as config_file:
                self.config.readfp(config_file)
        self.config_file_path = path
        
        #setup default options if they don't exist   
        path_opts = [("root_dir",default_dir),
                     ("libpack_dir","%(root_dir)s"),
                     ("workspace","%(root_dir)s" + os.path.sep + "workspace")]
        self._set_config_defaults("Paths", path_opts)
        self._set_config_defaults("LibPack", [("name_template",
                                              "FCLibs_{arch}_{toolchain}")])
        
        if self.config.has_option("LibPack", "path"):
            #use an existing LibPack
            self._setup_from_existing()
            
    def _set_config_defaults(self, section, options):
        if not self.config.has_section(section):
            self.config.add_section(section)
        for item in options:
            if not self.config.has_option(section, item[0]):
                self.config.set(section, item[0], item[1])
                
    def _setup_from_existing(self):
        libpack_path = self.config.get("LibPack", "path")
        if os.path.exists(libpack_path):
            manifest_path = os.path.join(libpack_path, "MANIFEST.db")
            if os.path.exists(manifest_path):
                self._manifest_path = manifest_path
                self._setup_from_manifest()
                self.exists = True
                self.path = libpack_path
                return
        print("Config [LibPack] 'path' not set to valid LibPack:", libpack_path,
              file=sys.stderr)
            
    def _setup_from_manifest(self):
        if self._manifest_path != None:
            conn = sqlite3.connect(self._manifest_path)
            cursor = conn.cursor()
            r = cursor.execute("SELECT toolchain, arch FROM info").fetchone()
            self.toolchain = r[0]
            self.arch = r[1]
            conn.commit()
            conn.close()
        
    def _setup_manifest(self):
        #must be called after self.path is set
        self._manifest_path = os.path.join(self.path, "MANIFEST.db")
        conn = sqlite3.connect(self._manifest_path)
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE installed"
                       "(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "name TEXT UNIQUE, version TEXT)")
        cursor.execute("CREATE TABLE files (id INT, name TEXT)")

        cursor.execute("CREATE TABLE info (toolchain TEXT, arch TEXT)")
        cursor.execute("INSERT INTO info VALUES (?,?)", (self.toolchain, self.arch))

        conn.commit()
        conn.close()

    def _load_build_formulas(self, formula_pkg):
        for importer, name, ispkg in pkgutil.iter_modules(formula_pkg.__path__):
            full_name = "BuildFormulas." + name
            module = importer.find_module(name).load_module(full_name)
            
            valid = True
            attributes = ["name", "version", "source", "depends_on",
                          "build", "install"]
            
            if not hasattr(module, "meta"):
                setattr(module, "meta", False)
                
            if module.meta:
                #required attrs for meta formulas
                attributes = ["name", "depends_on"]

            for attr in attributes:
                if not hasattr(module, attr):
                    valid = False
                    print(module.__name__ + " has no attribute " + attr,
                          file=sys.stderr)
                    bad = module.__name__

            if not valid:
                raise ValueError("Invalid build formula: " + bad)
            
            self._build_formulas[module.name] = module

    def write_config_file(self):
        """
        Write in-memory configuration to disk
        """
        with open(self.config_file_path, "wb") as config_file:
            self.config.write(config_file)

    def manifest_add(self, lib_name, lib_version, filenames):
        """
        Add file or directory to manifest database
        """
        if self._manifest_path != None:
            conn = sqlite3.connect(self._manifest_path)
            cursor = conn.cursor()
            id_query = "SELECT id FROM installed WHERE name = ?"
            #make sure lib is not already inserted into installed table
            if cursor.execute(id_query, (lib_name,)).fetchone() == None:
                
                query = "INSERT INTO installed (name, version) VALUES (?,?)"
                cursor.execute(query, (lib_name, lib_version))

            lib_id = cursor.execute(id_query, (lib_name,)).fetchone()[0]
            
            for name in filenames:
                cursor.execute("INSERT INTO files VALUES (?,?)", (lib_id, name))

            conn.commit()
            conn.close()

    def manifest_remove(self, lib_name):
        """
        Remove all entries associated with lib_name
        """
        if self._manifest_path != None:
            conn = sqlite3.connect(self._manifest_path)
            cursor = conn.cursor()
            files_delete = None
            
            id_query = "SELECT id FROM installed WHERE name = ?"
            row = cursor.execute(id_query, (lib_name,)).fetchone()
            if row != None:
                lib_id = row[0]

                query = "SELECT name FROM files WHERE id = ?"
                files_delete = cursor.execute(query, (lib_id,)).fetchall()
                cursor.execute("DELETE FROM files WHERE id = ?", (lib_id,))

                cursor.execute("DELETE FROM installed WHERE id = ?", (lib_id,))

            conn.commit()
            conn.close()

            return files_delete

    def new(self, toolchain, arch):
        """
        Setup a new LibPack
        """

        name = self.config.get("LibPack", "name_template").format(
            toolchain=toolchain, arch=arch)
        libpack_path = os.path.join(self.config.get("Paths","libpack_dir"), name)

        if os.path.exists(libpack_path):
            raise ValueError("Directory already exsits: " + libpack_path)

        os.mkdir(libpack_path)
        os.mkdir(os.path.join(libpack_path, "include"))
        os.mkdir(os.path.join(libpack_path, "lib"))
        os.mkdir(os.path.join(libpack_path, "bin"))
        #os.mkdir(os.path.join(libpack_path, "share"))

        self.exists = True
        self.path = libpack_path
        self.toolchain = toolchain
        self.arch = arch
        
        self._setup_manifest()
        self.config.set("LibPack", "path", libpack_path)
        self.write_config_file()

        print("Successfully created empty LibPack:", self.path)

    def is_installed(self, name):
        conn = sqlite3.connect(self._manifest_path)
        cursor = conn.cursor()

        row = cursor.execute("SELECT * FROM installed WHERE name = ?",
                             (name,)).fetchone()
        conn.commit()
        conn.close()

        return row != None
    
    def install(self, name):
        if not self.exists:
            raise LibPackError("Config [LibPack] 'path' not set (have you run 'new'?)")

        if self.is_installed(name):
            print(name + " is already installed")
            return

        if self._build_formulas == {}:
            import BuildFormulas
            self._load_build_formulas(BuildFormulas)
            
        try:
            formula = self._build_formulas[name]
        except KeyError:
            raise LibPackError("No build formula found for " + name)

        #install dependencies
        for n in formula.depends_on:
            self.install(n)

        if not formula.meta:
            src_dir = utils.get_source(formula.source,
                                       self.config.get("Paths", "workspace"))
            old_cwd = os.getcwd()
            os.chdir(src_dir)
            
            try:
                print("Dependencies: {0}\n".format(formula.depends_on))    
                print("Building {0}...\n".format(name))
                formula.build(self)
                print("Installing {0}...\n".format(name))
                formula.install(self)
                print("Successfully installed {0}\n".format(name))
            except CalledProcessError as e:
                print(e)
                #start shell for debugging
                utils.run_cmd("cmd")
            
            os.chdir(old_cwd)
        

    def uninstall(self, name):
        if not self.is_installed(name):
            raise LibPackError(name + " is not installed")
        
        files_delete = self.manifest_remove(name)
        for item in files_delete:
            path = os.path.join(self.path, item[0])
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
        print("Successfully uninstalled " + name)
    


class Subcommand:
    def __init__(self, name, options=[], args=None, callback=None,
                 usage="", short_help="", detailed_help=""):
        self.name = name
        self.options = options
        self.args = args
        self.callback = callback
        self.usage = usage
        self.short_help = short_help
        self.detailed_help = detailed_help
        
    def parse_args(self, arg_list):
        help = self.short_help + "\n\n" + self.detailed_help
        parser = optparse.OptionParser(usage=self.usage, description=help)
        parser.add_options(self.options)
        opts, args = parser.parse_args(arg_list)
        
        if self.callback != None:
            self.callback(opts, args)
            
        parser.destroy()
        
class CommandParser(optparse.OptionParser):
    def __init__(self, usage=None, description=None):
        optparse.OptionParser.__init__(self, usage=usage, description=description)

        self.subcommands = {}

    def add_subcommand(self, name, options=[], args=None, callback=None,
                       usage="", short_help="", detailed_help=""):
        self.subcommands[name] = Subcommand(name, options, args, callback,
                                            usage, short_help, detailed_help)

    def add_option(self, *args, **kwargs):
        if "subcmd" in kwargs.keys():
            name = kwargs.pop("subcmd")
            self.subcommands[name].options.append(optparse.Option(*args, **kwargs))
        else:
            optparse.OptionParser.add_option(self, *args, **kwargs)

    def parse_args(self, args=None, values=None):
        if args == None:
            args = sys.argv[1:]

        if args[0] in self.subcommands.keys():
            self.subcommands[args[0]].parse_args(args[1:])
        else:
            optparse.OptionParser.parse_args(self, args, values)       

def on_new(options, args):
    #print(options, args)
    LIBPACK.new(args[0], options.arch)

def on_install(options, args):
    LIBPACK.install(args[0])

def on_uninstall(options, args):
    LIBPACK.uninstall(args[0])
    
def parse_command_line():
    parser = CommandParser()

    usage = "{0} {1} [options]"
    help = "Sets up a new LibPack"
    parser.add_subcommand("new", callback=on_new,
                          usage=usage.format("new","TOOLCHAIN"), short_help=help)
    parser.add_option("-a", subcmd="new", dest="arch",
                      choices=["x86","x64"], default="x86",
                      help="Set build architecure {x86, x64} [default: %default]")

    help = "Install a library into the LibPack"
    parser.add_subcommand("install", callback=on_install,
                          usage=usage.format("install","FORMULA"),short_help=help)
    parser.add_subcommand("uninstall", callback=on_uninstall,
                          usage=usage.format("uninstall","FORMULA"))
    #parser.parse_args(["new", "vc9", "-a", "x86"])
    #parser.parse_args(["install", "freetype"])
    parser.parse_args()
    
def main():
    global LIBPACK
    try:
        LIBPACK = LibPack()
        parse_command_line()
    except (ValueError, LibPackError) as e:
        print(e, file=sys.stderr)
        
if __name__ == "__main__":
    main()
