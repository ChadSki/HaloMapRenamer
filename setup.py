import sys
from cx_Freeze import setup, Executable

setup(
    name = "On Dijkstra's Algorithm",
    version = "3.1",
    description = "A Dijkstra's Algorithm help tool.",
    executables = [Executable("mdrenamer.py")])
