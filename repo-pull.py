from git import Repo
from git import RemoteProgress
import os
import stat

#Made on Python 3.7.4 64-bit
#By Andrei Bornstein
#1/13/2021
#requires GitPython to run
#pip install gitpython
#Command Line Usage: repo-pull.py (run in directory that can hold the firmware folder)

class CloneProgress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        if message:
            print(message)

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def rmtree(top):
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWUSR)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(top)

def file_mod(file_path, mod_target, mod_val, dest_path=os.getcwd(), occurence=0):
    file = open(file_path, "r")
    file_data = file.readlines()
    file.close()
    line = [i for i in file_data if mod_target in i]
    file_data[file_data.index(line[occurence])] = mod_val + "\n"
    if os.path.exists(dest_path) and os.path.isfile(dest_path):
        dest_file = open(dest_path, "w")
        dest_file.truncate()
        dest_file.writelines(file_data)
        dest_file.close()
    else:
        mod_file = open(dest_path, "x")
        mod_file.writelines(file_data)
        mod_file.close()

prusa_repo_path = "https://github.com/prusa3d/Prusa-Firmware.git"
destination = os.getcwd() + "/Prusa-Firmware"
firm_path = "/Firmware/variants/"
firm_filename = "1_75mm_MK25S-RAMBo13a-E3Dv6full.h"
firm_configname = "config.h"
firm_mod_target= "Z_MAX_POS"

if os.path.exists(destination) and os.path.isdir(destination):
    rmtree(destination)
    print("Removed existing directory.")

Repo.clone_from(prusa_repo_path, destination, progress=CloneProgress())
cls()
os.chdir(destination + firm_path)
file_mod(firm_filename, firm_mod_target, "#define Z_MAX_POS 202", "../Configuration_prusa.h")
os.chdir("..")
file_mod(firm_configname, "LANG_MODE", "#define LANG_MODE 0", firm_configname, 1)
print("Fresh project cloned and ready")
