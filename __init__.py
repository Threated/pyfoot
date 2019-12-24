"""
Pyfoot
~~~~~~

Pyfoot is a high-level library for writing simple 2d games.
It is based upon the Python library pygame and can partly be used
"""

__author__ = "Jan Skiba"
__version__ = "0.1"
__license__ = "MIT"



if __name__ == "__main__":
    from .__main__ import init_folders
    init_folders()
else:                             
    from .main import *
    
    
