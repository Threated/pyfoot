from itertools import chain
from collections import OrderedDict
from inspect import isclass
from pathlib import Path

from .types import (pygame, MouseInfo, AnyColor, Union, Set, List, Tuple, Type, Optional, Color, TypeVar)
from . import constants
from .textinput import TextInput

WORLD: Optional["World"] = None
CLOCK = None
EVENTS: List[pygame.event.Event] = []


# TODO Test set_world, more Greenfoot. methods


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
        self.drawing_color: AnyColor = drawing_color
        self.drawing_width: int = drawing_width
        self._requires_update: bool = True

    @classmethod
    def from_surface(cls, surface: pygame.Surface) -> "Image":
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
    def from_path(cls, path: str) -> "Image":
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
        self._requires_update = True

    def scale_by(self, factor: float):
        """
        Scales the image linearly by a given factor

        :param factor: Factor to be scaled with
        :type factor: float
        """
        self.scale(int(self.width * factor), int(self.height * factor))

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
        self._requires_update = True


    def get_color_at(self, pos: Tuple[int, int]) -> Color:
        """
        Returns the color at a given position
        
        :param pos: The position to be checked
        :type pos: Tuple[int, int]
        :return: The color at the position
        :rtype: Color
        """
        return self.surface.get_at(pos)

    def draw_rect(self, width: int, height: int, pos: Tuple[int, int], color: AnyColor = None, line_width: int = None) -> None:
        """
        Draws a rectangle on the Image
        
        :param width: Width of the rectangle
        :type width: int
        :param height: Height of the rectangle
        :type height: int
        :param pos: Top left corner of the rectangle relative to the image
        :type pos: Tuple[int, int]
        :param color: Color of the rectangle, defaults to self.drawing_color
        :type color: AnyColor, optional
        :param line_width: outline width of the rectangle, defaults to self.drawing_width
        :type line_width: int, optional
        """
        color = color if color is not None else self.drawing_color
        line_width = line_width if line_width is not None else self.drawing_width
        pygame.draw.rect(self.surface, color, (*pos, width, height), line_width)
        self._requires_update = True

    def draw_circle(self, radius: Union[int, float], center: Tuple[int, int], color: AnyColor = None, width: int = None):
        """
        Draws a circle on the surface
        
        :param radius: Radius of the circle
        :type radius: Union[int, float]
        :param center: Center point of the circle
        :type center: Tuple[int, int]
        :param color: Color of the circle, defaults to self.drawing_color
        :type color: AnyColor, optional
        :param width: Width of the circle outline. If 0 fills the circle, defaults to self.drawing_width
        :type width: int, optional
        """
        width = width if width is not None else self.drawing_width
        color = color if color is not None else self.drawing_color
        pygame.draw.circle(self.surface, color, center, radius, width)
        self._requires_update = True

    def draw_line(self, start_point: Tuple[int, int], end_point: Tuple[int, int], color: AnyColor = None, width: int = None):
        """
        Draws a line on the image
        
        :param start_point: Start point of the line
        :type start_point: Tuple[int, int]
        :param end_point: End point of the line
        :type end_point: Tuple[int, int]
        :param color: Color of the line, defaults to self.drawing_color
        :type color: AnyColor, optional
        :param width: The width of the line, defaults to self.drawing_width
        :type width: int, optional
        """
        width = width if width is not None else self.drawing_width
        color = color if color is not None else self.drawing_color
        pygame.draw.line(self.surface, color, start_point, end_point, width)
        self._requires_update = True

    def draw_image(self, img: Union[pygame.Surface, "Image"], pos: Tuple[int, int] = (0, 0)):
        """
        Draws an Image or Surface on the Image
        
        :param img: Image or Surface to be drawn on the Image
        :type img: Union[pygame.Surface, Image]
        :param pos: Start position from where to draw, defaults to (0, 0)
        :type pos: Tuple[int, int], optional
        """
        if isinstance(img, Image):
            img = img.surface
        self.surface.blit(img, pos)
        self._requires_update = True

    def draw_text(self, text: Union[str, "Text"], pos: Tuple[int, int]):
        """
        Draws text on the image.
        
        :param text: The text to be drawn. For more customization a Text object can be supplied
        :type text: Union[str, Text]
        :param pos: The relative position of the Text on the Image
        :type pos: Tuple[int, int]
        """
        if type(text) is str:
            text = Text(text)  # type: ignore
        self.surface.blit(text.image.surface, pos)  # type: ignore
        self._requires_update = True

    def draw_polygon(self, points: List[Tuple[int, int]], width: int = None, color: AnyColor = None):
        """
        Draws a polygon on the surface.
        
        :param points: List of points to be drawn
        :type points: List[Tuple[int, int]]
        :param width: The width of the outline. If width is 0 the polygon will be filled, defaults to self.drawing_width
        :type width: int, optional
        :param color: The color to draw the polygon in. If not specified self.drawing_color will be used
        :type color: AnyColor, optional
        """
        color = color if color is not None else self.drawing_color
        width = width if width is not None else self.drawing_width
        pygame.draw.polygon(self.surface, color, points, width)
        self._requires_update = True

    def fill(self, color: AnyColor = None):
        """
        Fills the entire Image in the given color
        
        :param color: The color to fill the image with. If not specified self.drawing_color will be used
        :type color: AnyColor, optional
        """
        self.surface.fill(color if color is not None else self.drawing_color)
        self._requires_update = True


class Actor:

    def __init__(self, path: str = "default"):
        """
        Default constructor for Actor class

        :param path: The path to the Actors image, defaults to "default"
        :type path: str, optional
        """
        if path == "default":
            path = Path(__file__).parent / "default_images/pyfoot_logo.png"  # type: ignore
            self._image = Image.from_path(path.as_posix())  # type: ignore
        else:
            self._image = Image.from_path(path)
        self.x: int = 0
        self.y: int = 0
        self.x_offset = 0
        self.y_offset = 0
        if self.get_world().cell_size == 1:
            world_dim = self.get_world().width, self.get_world().height
            self.image.scale_by(min([min(1, min(i//4, j)/i) for i, j in zip(world_dim, self.image.get_dimensions())]))
            # scale the image accordingly so that the max size of the image is half of the screen size
        else:
            self.image.scale(self.get_world().cell_size, self.get_world().cell_size)
        self.trigger_on_relief: bool = False
        self.__rotation: float = 0
        self._prev_rect: Optional[pygame.Rect] = None
        self._rendered_img: pygame.Surface = self._image.surface.convert_alpha()

    @property
    def location(self) -> Tuple[int, int]:
        return self.x, self.y

    @property
    def rotation(self) -> float:
        return self.__rotation

    @rotation.setter
    def rotation(self, angle: Union[float, int]):
        while angle < 0:
            angle += 360
        while angle > 360:
            angle -= 360
        if not self.__rotation == angle:
            self.__rotation = angle
            self._image._requires_update = True

    def __repr__(self):
        return f"<{self.__class__} object at ({self.x}, {self.y})>"

    def get_world(self) -> "World":
        "Returns the world object the actor is in"
        if WORLD is None:
            raise Exception("Initialize a World first")
        return WORLD

    def to_image_pos(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        """
        Converts a pixel coordinate of the world to a pixel coordinate on the actors image.

        :param pos: Pixel coordinate of the world
        :type pos: Tuple[int, int]
        :return: Pixel coordinate on the actors image. Note that if the given pixel coordinate is not on the actors image this might give a coordinate that is outside of the actors image
        :rtype: Tuple[int, int]
        """
        return pos[0] - self.x * self.get_world().cell_size, pos[1] - self.y * self.get_world().cell_size


    def realign(self):
        "When using a grid world this method will realign the object to the center of the cell if it was offset by any kind of image manipulation"
        cell_size = self.get_world().cell_size
        if cell_size != 1:
            self.x_offset = (cell_size - self._image.width) // 2
            self.y_offset = (cell_size - self._image.height) // 2

    def set_location(self, x: int, y: int):
        """
        Sets the location of the actor.
        
        :param x: the x coordinate of the actor
        :type x: int
        :param y: the y coordinate of the actor
        :type y: int
        """
        self.x = x
        self.y = y

    def turn_towards(self, other: Union["Actor", Tuple[int, int]]):
        """
        Rotates the actor towards the other

        :param other: other actor
        :type other: Actor
        :raises TypeError: If the Argument is not a subclass of actor
        """

        if not isinstance(other, (tuple, Actor)):
            raise TypeError(f"Argument needs to be a subclass of Actor or a Tuple representing a Position not {type(other)}")
        m1 = pygame.math.Vector2(self.x * self.get_world().cell_size + (self._image.width // 2), self.y * self.get_world().cell_size + (self.image.height // 2))  # middle of self
        if isinstance(other, Actor):
            m2 = pygame.math.Vector2(other.x * self.get_world().cell_size + (other._image.width // 2), other.y * self.get_world().cell_size + (other.image.height // 2))  # middle of other
        else:
            m2 = pygame.math.Vector2(other)
        angle = (-m1 + m2).angle_to(pygame.math.Vector2(0, -1))  # angle of the resulting vector to a vertical line
        self.rotation = angle

    def get_closest(self, cls: Type["Actor"] = None) -> "Actor":
        """
        Gets the closest Actor object by Class

        :param cls: A superclass of Actor, default None means any Actor
        :type cls: Type[Actor], optional
        :return: The closest Actor of the specified class
        :rtype: Actor
        """
        cls = Actor if cls is None else cls
        pos = pygame.math.Vector2(self.x * self.get_world().cell_size, self.y * self.get_world().cell_size)
        return min([
            a
            for a in self.get_world().get_objects(cls)
            if a is not self],
            key=lambda obj: pos.distance_to(pygame.math.Vector2(obj.x * self.get_world().cell_size, obj.y * self.get_world().cell_size)))

    @property
    def image(self) -> Image:
        """
        Returns the image object of the actor without rotation

        :return: The image object of the actor
        :rtype: Image
        """
        return self._image

    @image.setter
    def image(self, img: Image):
        """
        Sets the a new image for the actor

        :param img: The new Image
        :type img: Image
        """
        self._image = img
        self._image._requires_update = True
        self.__render()

    def __render(self):
        """
        Internal method that renders the actors image with its current rotation.
        """
        self._rendered_img = pygame.transform.rotate(self._image.surface, self.__rotation)

    def mouse_over(self) -> bool:
        "Returns whether the mouse is over the actor"
        return self._image.surface.get_rect(x=self.x * self.get_world().cell_size, y=self.y * self.get_world().cell_size).collidepoint(pygame.mouse.get_pos())

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
            elif self.trigger_on_relief and self.mouse_over():
                self.trigger_on_relief = False
                return True
            else:
                return False
        else:
            if self.mouse_over() and pygame.mouse.get_pressed()[buttons[mouse_button]]:
                self.trigger_on_relief = True
                return False
            elif self.trigger_on_relief and self.mouse_over():
                self.trigger_on_relief = False
                return True
            else:
                self.trigger_on_relief = False
                return False

    def _update(self, world: "World") -> Optional[List[pygame.Rect]]:
        """Internal method that draws the actor to the screen and returns the area that has to be updated"""
        new_pos = (self.x * world.cell_size + self.x_offset, self.y * world.cell_size + self.y_offset)
        if self.image._requires_update or self._prev_rect is None or new_pos != self._prev_rect.topleft:
        # if actor image changed or actor moved or actor has not yet been drawn
            self.__render()
            self.image._requires_update = False
            areas_to_update: List[pygame.Rect] = []
            new_rect: pygame.Rect = self._rendered_img.get_rect(topleft=new_pos)
            render_before_all, render_after_all = [], []  # type: ignore
            all_rects = (new_rect, self._prev_rect) if self._prev_rect is not None else (new_rect,)
            for rect in all_rects:  # type: ignore
                rect = rect.clip(world.bg.surface.get_rect())
                if not rect.size == (0, 0):
                    rect = world._display.blit(world.bg.surface.subsurface(rect), rect.topleft)

                    def get_render_info(actor: Actor) -> Tuple[pygame.Surface, Tuple[int, int]]:
                        if actor._prev_rect is None:
                            actor._prev_rect = actor.image.surface.get_rect(x=actor.x * world.cell_size, y=actor.y * world.cell_size)
                        sub_rect = rect.clip(actor._prev_rect)
                        pos = sub_rect.topleft
                        sub_rect.topleft = actor.to_image_pos(pos)
                        return actor._rendered_img.subsurface(sub_rect), pos
                    
                    areas_to_update.append(rect)
                    other_objs = world.get_objects()
                    if len(other_objs) > 1:
                        self_i = other_objs.index(self)
                        render_before, render_after = other_objs[:self_i], other_objs[self_i + 1:]
                        overlapping_actors = map(lambda idx: render_before[idx], rect.collidelistall(
                            list(map(lambda act: act._rendered_img.get_rect(x=act.x * world.cell_size, y=act.y * world.cell_size), render_before))))  # may not work because not multiplied by cell_size
                        render_before_all.extend(map(get_render_info, overlapping_actors))
                        overlapping_actors = map(lambda idx: render_after[idx], rect.collidelistall(
                            list(map(lambda act: act._rendered_img.get_rect(x=act.x * world.cell_size, y=act.y * world.cell_size), render_after))))  # may not work because not multiplied by cell_size
                        render_after_all.extend(map(get_render_info, overlapping_actors))
            self._prev_rect = new_rect
            for render_info in render_before_all:
                areas_to_update.append(world._display.blit(*render_info))
            areas_to_update.append(world._display.blit(self._rendered_img, self._prev_rect.topleft))
            for render_info in render_after_all:
                areas_to_update.append(world._display.blit(*render_info))
            return areas_to_update
        return None

    def at_edge(self) -> bool:  # TODO: add top left right bottem
        width, height = self.get_world().width, self.get_world().height
        return self.x * self.get_world().cell_size + self._image.width > width or self.x * self.get_world().cell_size < 0 or self.y * self.get_world().cell_size + self._image.height > height or self.y * self.get_world().cell_size < 0

    def is_touching(self, other: Union[Type["Actor"], "Actor"]) -> bool:
        """
        Tests if the image of the current actor touches the image of another object or object of a specified class

        :param other: Can be an object or class that inherits from Actor
        :type other: Union[Type[Actor], Actor]
        :return: Returns wheather the obj touches the specified object or an object of the specified class
        :rtype: bool
        """
        if isclass(other):
            for actor in self.get_world().get_objects(other):  # type: ignore
                if actor is self:
                    continue
                return self._rendered_img.get_rect(x=self.x * self.get_world().cell_size, y=self.y * self.get_world().cell_size).colliderect(actor._rendered_img.get_rect(x=actor.x * self.get_world().cell_size, y=actor.y * self.get_world().cell_size))
            return False
        else:
            return self._rendered_img.get_rect(x=self.x * self.get_world().cell_size, y=self.y * self.get_world().cell_size).colliderect(other._rendered_img.get_rect(x=other.x * self.get_world().cell_size, y=other.y * self.get_world().cell_size))

    def get_intersecting(self, other: Type["Actor"]) -> Optional["Actor"]:
        """
        Given a Class returns the first instance intersecting this object else None
        
        :return: The first intersecting actor if any else None
        :rtype: Optional[Actor]
        """
        for actor in self.get_world().get_objects(other):
            if actor is self:
                continue
            elif self._rendered_img.get_rect(x=self.x * self.get_world().cell_size, y=self.y * self.get_world().cell_size).colliderect(actor._rendered_img.get_rect(x=actor.x * self.get_world().cell_size, y=actor.y * self.get_world().cell_size)):
                return actor
        return None

    def act(self) -> None:
        "This method is run every frame and can be overridden by any subclass to implement new functionality"
        pass


class Text(Actor):

    def __init__(self, message: str, fontsize: int = 15, font: str = "Arial", color: AnyColor = Color(0, 0, 0), editable: bool = False, focused: bool = True):
        super().__init__()
        self.textbox: TextInput = TextInput(message, font_family=font, font_size=fontsize, text_color=color)
        if not editable:
            self.textbox.cursor_switch_ms = -1
        self.textbox.update([])
        self.image = Image.from_surface(self.textbox.surface)
        self.editable: bool = editable
        self.focus: bool = False

    @property
    def message(self) -> str:
        return self.textbox.get_text()

    @message.setter
    def message(self, text: str) -> None:
        self.textbox.input_string = text
        self.textbox.update([])
        self.image = Image.from_surface(self.textbox.surface)
    
    def act(self):
        """
        This is the default act Method of pyfoot.Text, which if self.editable serves the purpose of only registering input if it has been clicked.
        Note if you want to keep this behavior and add a act method to your class which inherits from this class make sure to call super().act()
        If you want to override this behavior make sure to update the textbox every frame like this 'self.textbox.update(pyfoot.get_all_events())'
        """
        if self.editable:
            if self.clicked():
                self.focus = True
            elif any(pygame.mouse.get_pressed()) and not self.mouse_over():
                self.focus = False

            if self.focus:
                self.textbox.cursor_switch_ms = 500
                self.textbox.update(EVENTS)
                self.message = self.textbox.input_string
            else:
                self.textbox.cursor_switch_ms = -1
                self.message = self.message


class World:

    def generate_default_background(self):
        """
        Draws a the default background for the World
        """
        img = Image(self.width, self.height)
        if self.cell_size == 1:
            img.fill((255, 255, 255))
            corner = (self.width, self.height)
            for i in range(0, self.width, 30):
                img.draw_line((i, 0), (corner[0], corner[1] - i))
                # img.draw_line((i, corner[1]), (corner[0], i))
            for i in range(0, self.height, 30):
                img.draw_line((0, i), (corner[0] - i, corner[1]))
        else:
            cell_img = Image(self.cell_size, self.cell_size)
            cell_img.fill((255, 255, 255))
            cell_img.drawing_width = 3
            cell_img.draw_rect(self.width, self.height, (0, 0))
            cell_img.scale(self.cell_size, self.cell_size)
            for width in range(0, self.width, self.cell_size):
                for height in range(0, self.height, self.cell_size):
                    img.draw_image(cell_img, (width, height))
        self.bg: Image = img


    def __init__(self, width: int, height: int, cell_size: int = 1, auto_init: bool = True):
        """
        Constructor for World

        :param width: Width of the World
        :type width: int
        :param height: Height of the World
        :type height: int
        :param cell_size: If greater than 1 makes a grid world where actors move in squares, defaults to 1
        :type cell_size: int, optional
        :param auto_init: [description], defaults to True
        :type auto_init: bool, optional
        """
        self.height: int = height * cell_size
        self.width: int = width * cell_size
        self.cell_size: int = max(cell_size, 1)
        if auto_init:
            global WORLD
            WORLD = self
            self._display: pygame.Surface = pygame.display.set_mode((self.width, self.height))
            set_world(self)
        self.actors: OrderedDict[Type[Actor], Set[Actor]] = OrderedDict()
        self.generate_default_background()
        self.speed = 60 if self.cell_size == 1 else 10

    def set_speed(self, speed: int):
        """
        Changes the game speed. This effects how often the game- and eventloop are run.

        :param speed: The game speed, default value is 60
        :type speed: int
        """
        self.speed = speed

    def set_bg(self, path: Union[str, Image, AnyColor], full_image: bool = False):
        """
        Sets the background of the world. Takes a path or an image object as an argument.
        Additional argument full_image can be said to True if you want a full image background despite of a grid world
        """
        if isinstance(path, str):
            self.bg = Image.from_path(path)
        elif isinstance(path, (Color, tuple)):
            self.bg = Image(self.width, self.height)
            self.bg.fill(path)
            return  # Image does not require any more scaling
        else:
            self.bg = path
        if self.cell_size == 1 or full_image:
            self.bg.scale(self.width, self.height)
        else:
            img = Image(self.width, self.height)
            cell_img = self.bg
            cell_img.scale(self.cell_size, self.cell_size)
            for width in range(0, self.width, self.cell_size):
                for height in range(0, self.height, self.cell_size):
                    img.draw_image(cell_img, (width, height))
            self.bg = img

    def show_text(self, text: str, x: int, y: int):
        "Shows Text at a given position.\nNote that this class internally adds a Text object to the world"
        t = Text(text)
        t.set_location(x, y)
        self.add(t)

    def _update(self):
        "Method called internally to update the worlds surface"
        if self.bg._requires_update:
            self.bg._requires_update = False
            update_area = self._display.blit(self.bg.surface, (0, 0))
            for a in self.get_objects():
                self._display.blit(a._rendered_img, (a.x * self.cell_size + a.x_offset, a.y * self.cell_size + a.y_offset))
            return update_area

    def remove(self, *objs: Actor):
        "Removes an actor from the world"
        for act in objs:
            self.actors.get(type(act), set()).discard(act)

    def add(self, *objs: Actor):
        """
        Adds all given actors to the world
        """
        for act in objs:
            self.actors.setdefault(type(act), set()).add(act)

    def set_paint_order(self, *types: Type[Actor]):
        """
        Sets the order in which objects are drawn on the screen.
        first item => drawn first so behind others
        last item => drawn last so in front of others
        """
        order_dict = {v: k for k, v in dict(enumerate(types)).items()}
        for key in order_dict.keys():
            self.actors.setdefault(key, set())
        self.actors = OrderedDict(sorted(self.actors.items(), key=lambda item: order_dict.get(item[0], -1)))  # type: ignore


    def get_objects(self, cls: Type[Actor] = Actor) -> List[Actor]:
        """
        Gets all objects of the specified class in this world

        :param cls: The class all objects should be from, defaults to Actor
        :type cls: Type[Actor], optional
        :raises TypeError: If argument is not an instance of Actor
        :return: Returns all actors of the specified class
        :rtype: List[Actor]
        """
        if not issubclass(cls, Actor):
            raise TypeError(f"Argument cls needs to be a subclass of Actor not {type(cls)}")
        if cls == Actor:
            return list(chain.from_iterable(self.actors.values()))
        else:
            return list(self.actors.get(cls, set()))

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


def get_all_events() -> List[pygame.event.Event]:
    """
    Return all pygame events from pygame.events.get

    :return: [description]
    :rtype: List[pygame.event.Event]
    """
    return EVENTS


def set_world(new_world: World):  # TODO: test
    """
    Changes the world that is shown. Can be used to initialize a world that has been created with auto_init=False or reinitialize an old World.

    :param new_world: The new World that should be displayed
    :type new_world: World
    """
    global WORLD
    new_world._display = pygame.display.set_mode((new_world.width, new_world.height))
    WORLD = new_world


def get_mouse_info() -> MouseInfo:
    """
    Gets the position of the mouse on the screen

    :return: Tuple representing the point of the mouse
    :rtype: Tuple[int, int]
    """
    info = MouseInfo(
        pos=pygame.mouse.get_pos(),
        left=pygame.mouse.get_pressed()[0],
        right=pygame.mouse.get_pressed()[1],
        middle=pygame.mouse.get_pressed()[2]
    )
    return info


def set_icon(icon: Union[Image, str]) -> None:
    """
    Sets the icon at the topleft of the window

    :param icon: The icon
    :type icon: Image
    """
    if isinstance(icon, str):
        icon = Image.from_path(icon)
    icon.scale(64, 64)
    pygame.display.set_icon(icon.surface)


def get_color_at(x: int, y: int) -> Color:
    """
    Gets the color of the world at a specified pixel location

    :param x: x coordinate
    :type x: int
    :param y: y coordinate
    :type y: int
    :raises Exception: Can not get the Color of a World if it has not yet been initialized
    :return: A Color object reqreseting the Color at the given position
    :rtype: Color
    """
    if WORLD is not None:
        return WORLD._display.get_at((x, y))
    else:
        raise Exception('Create a World first before calling pyfoot.get_color_at')


def start():
    """
    Starts the execution of the gameloop

    :raises Exception: Raises an exception if there was no World object initialized before execution of this mehtod. This can be Done by calling pyfoot.setWorld or by creating a default World object
    """

    if WORLD is None:
        raise Exception('Create a World first before calling pyfoot.start')
        stop()
    global CLOCK, EVENTS
    CLOCK = pygame.time.Clock()
    running = True
    while running:
        # eventloop
        CLOCK.tick(WORLD.speed)
        EVENTS = pygame.event.get()
        for event in EVENTS:
            if event.type == pygame.QUIT:
                stop()

        update = WORLD._update()
        if update is not None:
            pygame.display.update(update)
        WORLD.act()
        for actor in WORLD.get_objects():
            actor.act()
            update = actor._update(WORLD)
            if update is not None:
                pygame.display.update(update)
