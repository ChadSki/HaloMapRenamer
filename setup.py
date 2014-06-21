import sys
from cx_Freeze import setup, Executable

setup(
    options = {"build_exe": {'build_exe': 'build'}},
    executables = [Executable("renamer.py")])
