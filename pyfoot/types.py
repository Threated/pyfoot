from typing import (Callable, Iterable, List, Optional, Set, Tuple, NamedTuple, Type,
                    Union, overload, TypeVar)

import sys
temp = sys.stdout
sys.stdout = None  # type: ignore
import pygame
sys.stdout = temp
del sys, temp
from pygame import Color

AnyColor = Union[Color, Tuple[int, int, int], Tuple[int, int, int, int]]
MouseInfo = NamedTuple("MouseInfo",[("pos", Tuple[int, int]), ("left", bool),("right", bool), ("middle", bool)])