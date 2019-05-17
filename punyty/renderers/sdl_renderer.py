import ctypes
from dataclasses import dataclass
import logging

import numpy as np
import sdl2
import sdl2.ext
from sdl2 import sdlgfx

from .renderer import Renderer
from punyty.vector import Vector3

logger = logging.getLogger(__name__)


def color_to_sdl(color):
    r, g, b = color
    return 0xff000000 \
        + (int(b * 255) << 16) \
        + (int(g * 255) << 8) \
        + int(r * 255)


@dataclass
class Joystick():
    x : float
    y : float


class SDLRenderer(Renderer):
    def __init__(self, width=800, height=600, f=2000, window_title="punyty", **kwargs):
        super().__init__(**kwargs)
        self.width = width
        self.height = height
        self.f = f
        sdl2.ext.init()

        # flags = sdl2.SDL_RENDERER_SOFTWARE
        flags = sdl2.SDL_WINDOW_OPENGL
        # flags = SDL_WINDOW_ALLOW_HIGHDPI
        # flags = 0
        self.window = sdl2.ext.Window(window_title, flags=flags, size=(width, height))
        # sdl2.SDL_SetSurfaceBlendMode(self.window.get_surface(), sdl2.SDL_BLENDMODE_BLEND)

        self.window.show()
        self.context = sdl2.ext.Renderer(self.window)
        self.joystick = Joystick(0, 0)
        self.clear_color = kwargs.get('clear_color', Vector3(0,0,0))

    def draw_axes(self, scene, length=1):

        axes = np.array([
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [1, 1, 1, 1],
        ], dtype=np.float)

        axes[:3, :] *= length

        points = [tuple(x) for x in self.vertices_to_screen(scene, axes).T.A]

        if len(points) < 4:
            return

        # each axis is (color, endpoints)
        lines = (
            (0xff0000ff, points[0], points[1]),
            (0xff00ff00, points[0], points[2]),
            (0xffff0000, points[0], points[3]),
        )

        for color, p1, p2 in lines:
            sdlgfx.aalineColor(self.context.sdlrenderer, p1[0], p1[1], p2[0], p2[1], color)

    def vertices_to_screen(self, scene, vertices):
        camera_matrix = scene.main_camera.matrix()
        transformed_vertices = np.linalg.inv(scene.main_camera.R) @ np.linalg.inv(scene.main_camera.T) @ vertices
        points = camera_matrix @ transformed_vertices

        # perspective
        points = points[:2, :] / points[2, :]

        points_int = points.round().astype(np.int32)
        return points_int

    def combine_vertices(self, vertices):
        pass

    def draw_line(self, points, color):
        x1, y1, x2, y2 = points
        color = color_to_sdl(color)
        renderer = self.context.sdlrenderer
        sdlgfx.aalineColor(renderer, x1, y1, x2, y2, color)

    def draw_poly(self, x1, y1, x2, y2, x3, y3, color):
        sdl_color = color_to_sdl(color)
        sdlgfx.filledTrigonColor(self.context.sdlrenderer, x1, y1, x2, y2, x3, y3, sdl_color)

    def clear(self):
        color = self.clear_color.as_tuple()
        self.context.clear(color_to_sdl(color))

    def prerender(self):
        # get events or sdl window won't show
        self.handle_events()

    def postrender(self):
        self.context.present()
        self.window.refresh()

    def quit(self):
        sdl2.ext.quit()

    def handle_events(self):
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == 113:  # q
                    raise Exception('user quit')

            elif event.type == sdl2.SDL_MOUSEMOTION:
                x, y = ctypes.c_int(0), ctypes.c_int(0) # Create two ctypes values
                _ = sdl2.mouse.SDL_GetMouseState(ctypes.byref(x), ctypes.byref(y))
                self.joystick.y = y.value / self.height
                self.joystick.x = x.value / self.width

            elif event.type == sdl2.SDL_QUIT:
                raise Exception('user quit')
