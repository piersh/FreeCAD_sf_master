from __future__ import print_function
import shutil
import os
import sys
from fnmatch import filter
import subprocess
import urllib

import patch

_original_env = os.environ.copy()
_commands = {}

class CommandNotFound(Exception):
    pass

def find_command(name):
    if sys.platform == "win32":
        name = name + ".exe"
        
    env_path = os.environ["PATH"].split(os.pathsep)
    env_path.extend(_original_env["PATH"].split(os.pathsep))
    
    for path in env_path:
        full_name = os.path.join(path, name)
        if os.path.isfile(full_name):
            return full_name
    raise CommandNotFound("Cannot find {0} in PATH".format(name))


def run_cmd(name, args=[], env=None, silent=False):
    if not env:
        env=os.environ
        
    if not _commands.has_key(name):
        _commands[name] = find_command(name)

    cmd_line = [_commands[name]]
    cmd_line.extend(args)
    
    if silent:
        with open(os.devnull, 'wb') as devnull:
            subprocess.check_call(cmd_line, stdout=devnull,
                                  stderr=devnull, env=env)
    else:
        subprocess.check_call(cmd_line, env=env)

def run_shell(args, env=None):
    return subprocess.call(args, shell=True, env=env)

def apply_patch(patch_filename, root_dir=None):
    p = patch.fromfile(patch_filename)
    return p.apply(root=root_dir)

def environ_from_bat(bat_file, args, initial_env=None):
    """
    Get environment modified by .bat file by parsing the output of set
    called in the same shell
    """
    cmd = 'cmd.exe /s /c ""{0}" {1} && echo OutputSeparator && set"'.format(
        bat_file, args)
    output = subprocess.check_output(cmd, shell=True, env=initial_env)
    env_dump = output.split("OutputSeparator")[1]

    new_environ = {}

    for line in env_dump.strip().split("\r\n"):
        pair = line.split("=")
        new_environ[pair[0].upper()] = pair[1]

    return new_environ

def setup_env(toolchain, arch):
    """
    Setup build environment for specified toolchain.
    """
    
    #Minimum PATH for Windows
    default_path = "C:\\Windows\\system32;C:\\Windows;C:\\Windows\\System32\\Wbem;"
    os.environ["PATH"] = default_path
    
    if toolchain.startswith("vc"):
        #trimming "vc" gets the version
        vs_dir = "Microsoft Visual Studio {0}.0".format(toolchain[2:])
        env_bat = "C:\\{0}\\{1}\\VC\\vcvarsall.bat"

        if os.path.exists(env_bat.format("Program Files (x86)", vs_dir)):
            env_bat = env_bat.format("Program Files (x86)", vs_dir)
        elif os.path.exists(env_bat.format("Program Files"), vs_dir):
            env_bat = path.format("Program Files", vs_dir)
        else:
            raise ValueError("Could not find vcvarsall.bat for " + toolchain)
            
        if arch == "x64":
            #first check if x64 tools are installed
            if subprocess.check_output([env_bat, "amd64"]) == '':
                os.environ = environ_from_bat(env_bat, "amd64")
            elif subprocess.check_output([env_bat, "x86_amd64"]) == '':
                os.environ = environ_from_bat(env_bat, "x86_amd64")
            else:
                raise ValueError(toolchain +
                                 " vcvarsall.bat cannot find a x64 toolchain")
        else:
            #arch == x86
            #vcvarsall.bat should allways be able to find x86 tools
            os.environ = environ_from_bat(env_bat, "x86")
        #print(os.environ["PATH"])
            
    #elif toolchain == "mingw64":


def _download_progress(blocks, block_size, file_size):
    percent = min(blocks*block_size*100.0 / file_size, 100)
    print("{0:3.1f}%".format(percent), end='\r')
    
def get_source(source, dest_dir):
    if source["type"] == "archive":
        filename = os.path.basename(source["url"])
        dest_file = os.path.join(dest_dir, filename)
        if not os.path.exists(dest_file):
            print("Downloading {0}...".format(filename))
            urllib.urlretrieve(source["url"], dest_file, _download_progress)
        #get directory name by extracting to empty directory
        print("Extracting...")
        tmp_dir = os.path.join(dest_dir, "tmp")
        if len(os.listdir(tmp_dir)) == 0:
            run_cmd("7z", ["x", "-y", "-o" + tmp_dir, dest_file], silent=True)
        
        src_dir = os.listdir(tmp_dir)[0]
        dest_src_dir = os.path.join(dest_dir, src_dir)
        
        #if os.path.exists(dest_src_dir):
            #shutil.rmtree(dest_src_dir)
            
        #os.rename(os.path.join(tmp_dir, src_dir), dest_src_dir)

        if not os.path.exists(dest_src_dir):
            os.rename(os.path.join(tmp_dir, src_dir), dest_src_dir)
            
        return dest_src_dir
    
    elif source["type"] == "git":
       run_cmd("git", ["clone", source["url"]])
       
def filter_files(names, *paterns):
    include_names = []
    for patern in paterns:
        include_names.extend(filter(names, patern))
    return include_names

def include_only_patterns(*paterns):
    """
    Inverse of shutil.ignore_patterns
    """
    def _ignore_names(path, names):
        include_names = filter_files(names, *paterns)
        ignore_names = []
        for name in names:
            if name not in include_names:
                ignore_names.append(name)
        return ignore_names        
    return _ignore_names

def copytree(src, dest_root, dest, symlinks=False, root=True, ignore=None):
    """"
    Copy an entire directory tree rooted at src.
    If root is False, only the contents of src is copied.
    """
    copied = []
    abs_dest = os.path.join(dest_root, dest)
    if not root:
        contents = os.listdir(src)
        
        ignore_names = []
        if ignore != None:
            ignore_names = ignore(src, contents)
        
        for name in contents:
            if name not in ignore_names:
                subsrc = os.path.join(src, name)

                if os.path.isfile(subsrc):
                    shutil.copy(subsrc, abs_dest)
                    copied.append(os.path.join(dest, os.path.basename(subsrc)))
                elif os.path.isdir(subsrc):
                    shutil.copytree(subsrc, os.path.join(abs_dest, name))
                    copied.append(os.path.join(dest, os.path.basename(subsrc)))
    else:
        shutil.copytree(src, abs_dest, symlinks, ignore)
        copied.append(os.path.join(dest, os.path.basename(src)))

    return copied
        
def move(src, dest_root, dest, root=True, ignore=None):
    """"
    Recursively move a file or directory.
    If root is False and src is a directory,
    only the contents of root_src is copied.
    """
    moved = []
    abs_dest = os.path.join(dest_root, dest)
    if not root and os.path.isdir(src):
        contents = os.listdir(src)
        
        ignore_names = []
        if ignore != None:
            ignore_names = ignore(src, contents)
        
        for name in contents:
            if name not in ignore_names:
                subsrc = os.path.join(src, name)
                shutil.move(subsrc, abs_dest)
                moved.append(os.path.join(dest, os.path.basename(subsrc)))
    else:
        shutil.move(src, abs_dest)
        moved.append(os.path.join(dest, os.path.basename(src)))

    return moved