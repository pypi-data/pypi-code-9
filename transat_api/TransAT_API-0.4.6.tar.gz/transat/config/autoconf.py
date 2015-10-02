from distutils import spawn
import platform
import readline
import os
import glob

readline.parse_and_bind("tab: complete")

def get_python_bit_version():
    return platform.architecture()[0]

def get_lib_suffix():
    if os.name == "nt":
        return "dll"
    else:
        return "so"

def get_executable_path(name):
    path = spawn.find_executable(name)
    if path is None:
        path = ""
        while(not os.path.isdir(path)):
            print "The executable "+name+" could not be found in the PATH.\n " \
                  "Enter the full absolute path to the executable folder.\n" \
                  "i.e.: /RIP_MAX/metrailler/Softwares/ParaView-4.3.1-Linux-64bit/bin"
            path = raw_input("")
    if (os.path.isfile(path)):
        path = os.path.dirname(path)
    return path

def get_paraview_site_packages(bin_dir):
    path = os.path.dirname(bin_dir)
    dir = None
    for root, dirs, files in os.walk(path):
        for file in files:
            if file == "simple.py":
                dir = os.path.dirname(os.path.join(root, file))
    if dir is None:
        print "Could not find paraview site-package directory"
        return None
    return os.path.dirname(dir)

def get_paraview_shared_libraries(bin_dir):
    path = os.path.dirname(bin_dir)
    dir = None
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith("."+get_lib_suffix()) and file.startswith("libvtk"):
                dir = os.path.dirname(os.path.join(root, file))
    if dir is None:
        return None
    dir = os.path.dirname(dir)
    return dir


path = get_executable_path("paraview")
print "site-packages :"+ get_paraview_site_packages(bin_dir=path)
print "shared "+get_paraview_shared_libraries(bin_dir=path)

