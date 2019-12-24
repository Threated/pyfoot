"""
Pyfoot
~~~~~~

Pyfoot is a high-level library for writing simple 2d games.
It is based upon the Python library pygame and was inspired by the java libary Greenfoot.
Most of the functions provided also accept pygame objects, which can provide more functionality.
"""

__author__ = "Jan Skiba"
__version__ = "0.1"
__license__ = "MIT"



if __name__ == "__main__":
    from __main__ import init_folders
    init_folders()
else:                             
    from main import *

