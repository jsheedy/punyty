import logging
import math
import sys

import numpy as np
import sdl2
import sdl2.ext
from sdl2 import sdlgfx

from .renderer import Renderer

logger = logging.getLogger(__name__)


class SDLRenderer(Renderer):
    def __init__(self, width=800, height=600, f=2000, window_title="punyty"):
        self.width = width
        self.height = height
        self.f = f
        self.frame = 0
        sdl2.ext.init()

        # sdl2.mouse.SDL_ShowCursor(0)
        flags = 0
        # flags = sdl2.SDL_RENDERER_SOFTWARE
        self.window = sdl2.ext.Window(window_title, flags=flags, size=(width, height))
        self.window.show()
        # self.surface = self.window.get_surface()
        self.context = sdl2.ext.Renderer(self.window)
        # self.context.clear(0)
        # self.context.present()
        # self.context.clear(0)

    def draw_axes(self, scene, length=1):

        axes = np.matrix([
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
        transformed_vertices = scene.main_camera.R.I * scene.main_camera.T.I * vertices
        # mask = (vertices[2, :] > 0).A[0]
        # forward_vertices = vertices[:, mask]
        # if np.any(transformed_vertices[2, :] < 0):
        #     return
        points = camera_matrix * transformed_vertices

        # perspective
        points = points[:2, :] / points[2, :]

        points_int = points.round().astype(np.int32)
        return points_int

    def combine_vertices(self, vertices):
        pass

    def draw_vertices(self, points, color=0xff00ff00):
        renderer = self.context.sdlrenderer

        # points= points.round().astype(np.int32)

        circle = sdlgfx.aacircleColor
        # circle = sdlgfx.filledCircleColor
        for x, y in points:
            circle(renderer, x, y, 2, color)

    def draw_line(self, x1, y1, x2, y2, color):
        # line = sdlgfx.aalineColor
        renderer = self.context.sdlrenderer
        sdlgfx.lineColor(renderer, x1, y1, x2, y2, color)

    def draw_polys(self, points, polys, color=0xff00ff00):
        renderer = self.context.sdlrenderer
        points= points.round().astype(np.int32)

        original_color = color


        line = sdlgfx.lineColor
        # line = sdlgfx.aalineColor
        for p1, p2, p3 in polys:

            x1, y1 = points[p1]
            x2, y2 = points[p2]
            line(renderer, x1, y1, x2, y2, color)

            x1, y1 = points[p1]
            x2, y2 = points[p3]
            line(renderer, x1, y1, x2, y2, color)

            x1, y1 = points[p2]
            x2, y2 = points[p3]
            line(renderer, x1, y1, x2, y2, color)

    def clear(self):
        self.context.clear(0)

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

            elif event.type == sdl2.SDL_QUIT:
                raise Exception('user quit')

