from __future__ import annotations

import sys
import math
from inspect import isclass
from pathlib import Path
from typing import (Callable, Iterable, List, Optional, Set, Tuple, Type,
                    Union, overload)


temp = sys.stdout
sys.stdout = None  # type: ignore
from . import constants
import pygame
from pygame import Color
from pygame.mixer import Sound
sys.stdout = temp
del sys, temp
WORLD: Optional["World"] = None
CLOCK = None

AnyColor = Union[Color, Tuple[int, int, int], Tuple[int, int, int, int]]
# TODO Polish, Rendering maybe, testing, more Greenfoot. methods


class Image:
    """
    Class for drawing on images.
    This class internally uses the a pygame.Surface for all its drawing.
    Feel free to manipulate this surface outside of this class with any pygame.draw methods.
    These surfaces are used for the background of the actor class and basically everything visual.
    You can draw any Image on any other Image
    """

    def __init__(self, width: int, height: int, drawing_color: AnyColor = Color(0, 0, 0), drawing_width: int = 1):
        """
        Creates a blank image to draw on
        
        :param width: Width of the image
        :type width: int
        :param height: Height of the image
        :type height: int
        :param drawing_color: The color which the draw methods are going to draw with, defaults to Black
        :type drawing_color: AnyColor, optional
        :param drawing_width: Defines how thick the lines drawn by the draw methods will be (0 is typically fill), defaults to 1
        :type drawing_width: int, optional
        """
        self.surface: pygame.Surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.drawing_color = drawing_color
        self.drawing_width = drawing_width

    @classmethod
    def from_surface(cls, surface: pygame.Surface) -> Image:
        """
        Creates an image object from a pygame.Surface
        
        :param surface: The surface
        :type surface: pygame.Surface
        :return: The new image object
        :rtype: Image
        """
        surf = cls(0, 0)
        surf.surface = surface
        return surf

    @classmethod
    def from_path(cls, path: str) -> Image:
        """
        Creates an image from a file. Supported types include 'jpg', 'jpeg', 'png', 'gif'
        
        :param path: path to the image resource
        :type path: str
        :raises NotImplementedError: The file type is not supported
        :raises FileNotFoundError: The given file was not found
        :return: The new Image object
        :rtype: Image
        """
        p = Path(path)
        if p.exists():
            if p.is_file() and p.suffix[1:] in ('jpg', 'jpeg', 'png', 'gif'):
                return cls.from_surface(pygame.image.load(str(p.absolute())))
            elif p.is_file():
                raise NotImplementedError(f"File type {p.suffix} is not supported")
            else:
                raise FileNotFoundError(f"The given path points to a folder not a file")
        else:
            raise FileNotFoundError(f"{p.as_posix()} does not exist")

    def scale(self, width: int, height: int):
        """
        Scales the image to a given size
        
        :param width: Future width
        :type width: int
        :param height: Future height
        :type height: int
        """
        self.surface = pygame.transform.scale(self.surface, (width, height))

    def scale_by(self, factor: float):
        """
        Scales the image linearly by a given factor
        
        :param factor: Factor to be scaled with
        :type factor: float
        """
        self.scale(int(self.width*factor), int(self.height*factor))

    def get_dimensions(self) -> Tuple[int, int]:
        """
        Returns the width and height as a tuple
        
        :return: Returns width and height as a tuple of (width, height)
        :rtype: Tuple[int, int]
        """
        return self.surface.get_rect().size

    @property
    def width(self) -> int:
        return self.get_dimensions()[0]

    @width.setter
    def width(self, width: int):
        self.scale(width, self.height)

    @property
    def height(self) -> int:
        return self.get_dimensions()[1]

    @height.setter
    def height(self, height: int):
        self.scale(self.width, height)

    def rotate(self, degrees: Union[float, int]) -> None:
        self.surface = pygame.transform.rotate(self.surface, degrees)

    def expand_to(self, *points: Tuple[int, int]) -> None:
        "Expands the surface so that the given point(s) is inside"
        needed_width, needed_height = self.width, self.height
        negative_width, negative_height = 0, 0
        for x, y in points:
            if x > needed_width:
                needed_width = x
            elif x < negative_width:
                negative_width = abs(x)
            if y > needed_height:
                needed_height = y
            elif y < negative_height:
                negative_height = abs(y)

        if needed_width > self.width or needed_height > self.height or not (negative_width == 0 and negative_height == 0):
            new_surface = pygame.Surface((needed_width + negative_width, needed_height + negative_height), pygame.SRCALPHA)
            new_surface.blit(self.surface, (negative_width, negative_height))
            self.surface = new_surface

    def get_color_at(self, pos: Tuple[int, int]) -> Color:
        return self.surface.get_at(pos)

    def draw_rect(self, width: int, height: int, pos: Tuple[int, int], color: AnyColor = None) -> None:
        color = color if color is not None else self.drawing_color
        pygame.draw.rect(self.surface, self.drawing_color, (*pos, width, height), self.drawing_width)

    def draw_circle(self, radius: Union[int, float], center: Tuple[int, int], color: AnyColor = None):
        color = color if color is not None else self.drawing_color
        pygame.draw.circle(self.surface, self.drawing_color, center, radius, self.drawing_width)

    def draw_line(self, start_point: Tuple[int, int], end_point: Tuple[int, int], color: AnyColor = None):
        color = color if color is not None else self.drawing_color
        pygame.draw.line(self.surface, color, start_point, end_point, self.drawing_width)

    def draw_image(self, img: Union[pygame.Surface, Image], pos: Tuple[int, int] = (0, 0)):
        if isinstance(img, Image):
            img = img.surface
        self.surface.blit(img, pos)

    def draw_text(self, text: Union[str, Text], pos: Tuple[int, int], color: AnyColor = None):
        color = color if color is not None else self.drawing_color
        if type(text) is str:
            text = Text(text, color=color)  # type: ignore
        self.surface.blit(text.image.surface, pos)  # type: ignore

    def draw_polygon(self, points: Iterable[Tuple[int, int]], width: int = None, color: AnyColor = None):
        color = color if color is not None else self.drawing_color
        width = width if width is not None else self.drawing_width
        pygame.draw.polygon(self.surface, self.drawing_color, points, width)

    def fill(self, color: AnyColor = None):
        self.surface.fill(color if color is not None else self.drawing_color)


class Actor:

    def __init__(self, path: str = "default"):
        """
        Default constructor for Actor class

        :param path: The path to the Actors image, defaults to "default"
        :type path: str, optional
        """
        self.image: Image
        if path == "default":
            path = Path(__file__).parent / "default_images/pyfoot_logo.png" # type: ignore
            self.image = Image.from_path(path.as_posix()) # type: ignore
        else:
            self.image = Image.from_path(path)
        self._x: int = 0
        self._y: int = 0
        self.x_offset = 0
        self.y_offset = 0
        if self.get_world().cell_size == 1:
            self.scale(50, 50)
        else:
            self.scale(self.get_world().cell_size, self.get_world().cell_size)
        self.trigger_on_relief: bool = False
        self._rotation: float = 0

    def rotate(self, angle: Union[int, float]):
        self.image.rotate(angle)
        self._rotation += angle

    @property
    def rotation(self) -> float:
        return self._rotation

    @rotation.setter
    def rotation(self, rotation: Union[float, int]):
        while rotation < 0:
            rotation += 360
        while rotation > 360:
            rotation -= 360
        self.image.rotate(rotation - self._rotation)
        print(f"Rotating image by {rotation-self._rotation}\nRotation is now by {rotation}")
        self._rotation = rotation

    def __repr__(self):
        return f"<{self.__class__} object at ({self.x}, {self.y})>"

    def get_world(self) -> "World":
        "Returns the world object the actor is in"
        if WORLD is None:
            raise Exception("Initialize a World first")
        return WORLD

    def to_image_pos(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        return pos[0] - self._x, pos[1] - self._y

    def scale(self, w: int, h: int):
        self.image.scale(w, h)
        self.realign()

    def realign(self):
        "When using a grid world this method will realign the object to the center of the cell if it was offset by any kind of image manipulation"
        cell_size = self.get_world().cell_size
        if cell_size != 1:
            self.x_offset = (cell_size - self.image.width) // 2
            self.y_offset = (cell_size - self.image.height) // 2

    def set_location(self, x: int, y: int):
        self.x = x
        self.y = y

    def turn_towards(self, other: Actor):
        """
        Rotates the actor towards the other
        
        :param other: other actor
        :type other: Actor
        :raises TypeError: If the Argument is not a subclass of actor
        """
        if not isinstance(other, Actor):
            raise TypeError(f"Argument needs to be a subclass of Actor not {type(other)}")
        m1 = pygame.math.Vector2(self._x + (self.image.width // 2), self._y + (self.image.height // 2))  # middle of self
        m2 = pygame.math.Vector2(other._x + (other.image.width // 2), other._y + (other.image.height // 2))  # middle of other
        angle = (-m1 + m2).angle_to(pygame.math.Vector2(0, -1))  # angle of the resulting vector to a vertical line
        self.rotation = angle

    def get_closest(self, cls: Type[Actor] = None) -> Actor:
        """
        Gets the closest Actor object by Class

        :param cls: A superclass of Actor, default None means any Actor
        :type cls: Type[Actor], optional
        :return: The closest Actor of the specified class
        :rtype: Actor
        """
        cls = Actor if cls is None else cls
        pos = pygame.math.Vector2(self._x, self._y)
        return min(
            [a
             for a in self.get_world().get_Objects(cls)
             if a is not self],
            key=lambda obj: pos.distance_to(pygame.math.Vector2(obj._x, obj._y)))

    def get_image(self) -> Image:
        """
        Returns the image object of the actor

        :return: The image object of the actor
        :rtype: Image
        """
        return self.image

    def mouse_over(self) -> bool:
        "Returns whether the mouse is over the actor"
        return self.image.surface.get_rect(x=self._x, y=self._y).collidepoint(pygame.mouse.get_pos())

    def clicked(self, mouse_button: str = None) -> bool:
        """
        Return whether the mouse clicked the object

        :param mouse_button: Can be set to test which mouse button was pressed. Argument can be set to left, right, middle or the default None, which means any click will count
        :type mouse_button: str, optional
        :return: Return whether the mouse clicked the object
        :rtype: bool
        """
        buttons = {"left": 0, "right": 1, "middle": 2}
        if mouse_button is None:
            if self.mouse_over() and any(pygame.mouse.get_pressed()):
                self.trigger_on_relief = True
                return False
            elif self.trigger_on_relief:
                self.trigger_on_relief = False
                return True
            else:
                return False
        else:
            if self.mouse_over() and pygame.mouse.get_pressed()[buttons[mouse_button]]:
                self.trigger_on_relief = True
                return False
            elif self.trigger_on_relief:
                self.trigger_on_relief = False
                return True
            else:
                return False

    def _update(self, display) -> pygame.Rect:
        return display.blit(self.image.surface, (self._x + self.x_offset, self._y + self.y_offset))

    def at_edge(self) -> bool:  # TODO: add top left right bottem
        width, height = self.get_world().width, self.get_world().height
        return self._x + self.image.width > width or self._x < 0 or self._y + self.image.height > height or self._y < 0

    @property
    def x(self) -> int:
        return self._x // self.get_world().cell_size

    @x.setter
    def x(self, value) -> None:
        self._x = value * self.get_world().cell_size

    @property
    def y(self) -> int:
        return self._y // self.get_world().cell_size

    @y.setter
    def y(self, value) -> None:
        self._y = value * self.get_world().cell_size

    def isTouching(self, other: Union[Type[Actor], Actor]) -> bool:
        """
        Tests if the image of the current actor touches the image of another object or object of a specified class

        :param other: Can be an object or class that inherits from Actor
        :type other: Union[Type[Actor], Actor]
        :return: Returns wheather the obj touches the specified object or an object of the specified class
        :rtype: bool
        """
        if isclass(other):
            for actor in self.get_world().get_Objects(other):  # type: ignore
                if actor is self:
                    continue
                return self.image.surface.get_rect(x=self._x, y=self._y).colliderect(actor.image.surface.get_rect(x=actor._x, y=actor._y))
            return False
        else:
            return self.image.surface.get_rect(x=self._x, y=self._y).colliderect(other.image.surface.get_rect(x=other._x, y=other._y))

    def get_intersecting(self, other: Type[Actor]) -> Optional[Actor]:
        for actor in self.get_world().get_Objects(other):
            if actor is self:
                continue
            elif self.image.surface.get_rect(x=self._x, y=self._y).colliderect(actor.image.surface.get_rect(x=actor._x, y=actor._y)):
                return actor
        return None

    def act(self) -> None:
        "This method is run every frame and can be overridden by any subclass to implement new functionality"
        pass


class Text(Actor):

    def render(self) -> None:
        "Updates the text, color and background color of the object"
        self.image = Image.from_surface(self.font.render(self.message, True, self.color, self.bg))

    def __init__(self, message: str, fontsize: int = 15, font: Union[pygame.font.Font, str] = "Arial", color: AnyColor = Color(0, 0, 0), bg: AnyColor = None):
        super().__init__()
        self._message: str = message
        self.bg: Optional[Color] = bg
        self.color: AnyColor = color
        self.font: pygame.font.Font
        if type(font) == str:
            try:
                self.font = pygame.font.SysFont(font, fontsize)
            except Exception:
                print(f"Did not find a System font named {font} defaulting to Arial")
                self.font = pygame.font.SysFont("Arial", fontsize)
        else:
            self.font = font
            self.font.size = fontsize
        self.render()

    @property
    def message(self) -> str:
        return self._message

    @message.setter
    def message(self, text: str) -> None:
        self._message = text
        self.render()


class World:

    def generate_default_background(self):

        img = Image(self.width, self.height)
        if self.cell_size == 1:
            img.fill((255, 255, 255))
            corner = (self.width, self.height)
            for i in range(0, self.width, 30):
                img.draw_line((i, 0), (corner[0], corner[1] - i))
                # img.draw_line((i, corner[1]), (corner[0], i))
            for i in range(0, self.height, 30):
                img.draw_line((0, i), (corner[0] - i, corner[1]))
                # img.draw_line((0, i), (i, 0))

        else:
            img.fill((255, 255, 255))
            img.drawing_width = 3
            img.draw_rect(self.width, self.height, (0, 0))
            img.scale(self.cell_size, self.cell_size)
        self.bg: Union[Image, AnyColor] = img

    def __init__(self, width: int, height: int, cell_size: int = 1, auto_init: bool = True):
        self.height: int = height * cell_size
        self.width: int = width * cell_size
        self.cell_size: int = cell_size
        if auto_init:
            global WORLD
            WORLD = self
            self._display: pygame.Surface = pygame.display.set_mode((self.width, self.height))
        self.actors: Set[Actor] = set()
        self.generate_default_background()
        self.speed = 60

    def set_speed(self, speed):
        self.speed = speed

    def set_bg(self, path: Union[str, Image], full_image: bool = False):
        """
        Sets the background of the world. Takes a path or an image object as an argument.
        Additional argument full_image can be said to True if you want a full image background despite of a grid world
        """
        if isinstance(path, str):
            self.bg = Image.from_path(path)
        else:
            self.bg = path
        if self.cell_size == 1 or full_image:
            self.bg.scale(self.width, self.height)
        else:
            self.bg.scale(self.cell_size, self.cell_size)

    def show_text(self, text: str, x: int, y: int):
        "Shows Text at a given position.\nNote that this class internally adds a Text object to the world"
        self.add_Object(Text(text), x, y)

    def update(self):
        "Method called internally to update the worlds surface"
        # Possibilities: 1. single color 2. picture 3. one picture per tile
        CLOCK.tick(self.speed)
        if isinstance(self.bg, Image):
            if self.cell_size == 1:
                self._display.blit(self.bg.surface, (0, 0))
            else:
                for width in range(0, self.width, self.cell_size):
                    for height in range(0, self.height, self.cell_size):
                        self._display.blit(self.bg.surface, (width, height))
        else:
            self._display.fill(self.bg)

    def add_Object(self, obj: Actor, x: int = None, y: int = None):
        "Adds an actor to the world at a given position"
        if x is not None and y is not None:
            obj.set_location(x, y)
        self.actors.add(obj)

    def remove_Object(self, obj: Actor):
        "Removes an actor from the world"
        self.actors.discard(obj)

    def add_Objects(self, *objs: Actor):
        "Add multiple actors at once at the position specified in the actors attributes."
        self.actors.update(objs)

    def get_Objects(self, cls: Type[Actor] = Actor) -> List[Actor]:
        return [act
                for act in self.actors
                if isinstance(act, cls)]

    def act(self):
        "This method is run every frame and can be overridden by any subclass to implement new functionality."
        pass


def stop():
    """
    Stops the program
    """
    pygame.quit()
    quit()


def set_title(name: str):
    """Sets the title of the window."""
    pygame.display.set_caption(name)


def is_key_down(key: str) -> bool:
    """
    Tests wheather a certain key is pressed

    :param key: The key that should be tested for
    :type key: str
    :return: Returns wheather the key is pressed or not
    :rtype: bool
    """
    pykey = constants.keys.get(key)
    if pykey is None:
        raise KeyError("The key you where checking for was not found. For A list of all keys run pyfoot.get_all_keys")
    return pygame.key.get_pressed()[pykey]


def get_all_keys() -> List[str]:
    """
    List of all keys that can be used for pyfoot.is_key_down

    :return: The List of keys
    :rtype: List[str]
    """
    return list(constants.keys.keys())


def set_world(new_world: World):
    "Changes the world that is shown. Can be used to initialize a world that has been created with auto_init=False or reinitialize an old World."
    global WORLD
    new_world._display = pygame.display.set_mode((new_world.width, new_world.height))
    WORLD = new_world


def get_color_at(x: int, y: int) -> Color:
    "Returns the Color at a given point on the world."
    if WORLD is not None:
        return WORLD._display.get_at((x, y))
    else:
        raise Exception('Create a World first before calling pyfoot.get_color_at')


def start():
    """
    Starts the execution of the gameloop

    :raises Exception: Raises an exception if there was no World object initialized before execution of this mehtod. This can be Done by calling pyfoot.setWorld or by creating a default World object
    """

    global CLOCK
    CLOCK = pygame.time.Clock()
    if WORLD is None:
        raise Exception('Create a World first before calling pyfoot.start')
        stop()
    CLOCK.tick(WORLD.speed)
    running = True
    while running:
        # eventloop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop()

        # TODO: Maybe overthink this rendering part
        WORLD.update()
        WORLD.act()
        for actor in WORLD.actors:
            actor.act()
            actor._update(WORLD._display)

        pygame.display.flip()


pygame.init()
