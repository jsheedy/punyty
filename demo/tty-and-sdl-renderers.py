""" two renderers at once """
import time

from punyty.vector import Vector3
from punyty.objects import Cube, Tetrahedron
from punyty.renderers import TTYRenderer, SDLRenderer
from punyty.scene import Scene


if __name__ == '__main__':
    width = 800
    height = 800
    scene = Scene()
    cube = Cube()
    scene.add_object(cube)
    tty_renderer = TTYRenderer()
    sdl_renderer = SDLRenderer(width=width, height=height)

    while True:
        t = time.time()
        cube.rotate(Vector3(t, t, t))
        scene.update()
        tty_renderer.render(scene, draw_edges=False, draw_polys=True)
        sdl_renderer.render(scene, draw_edges=False, draw_polys=True)
