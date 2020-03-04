"""
Pyfoot
~~~~~~

Pyfoot is a high-level library for writing simple 2d games.
It is based upon the Python library pygame and was inspired by the java library Greenfoot.
Most of the functions provided also accept pygame objects, which can provide more functionality.
"""

__author__ = "Jan Skiba"
__version__ = "0.1"
__license__ = "GNU 3"


from .main import (
    Actor,
    Text,
    pygame,
    World,
    Image,
    AnyColor,
    get_mouse_info,
    get_all_keys,
    get_color_at,
    get_all_events,
    is_key_down,
    set_title,
    set_icon,
    set_world,
    stop,
    start
)

from pygame.mixer import Sound
pygame.init()

# set default window icon
set_icon(__file__[:-len("__init__.py")] + "/default_images/pyfoot_logo.png")
if __name__ == "__main__":
    from .__main__ import init_folders
    init_folders()
