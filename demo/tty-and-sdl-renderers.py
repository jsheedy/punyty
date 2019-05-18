""" two renderers at once """
import time

from punyty.model import Model
from punyty.objects import Cube, Tetrahedron
from punyty.renderers import TTYRenderer, SDLRenderer
from punyty.scene import Scene
from punyty.vector import Vector3


if __name__ == '__main__':
    width = 800
    height = 800
    scene = Scene()
    scene.main_camera.position = Vector3(0,0,-15)
    cube = Cube()
    model = Model.load_ply('/Users/velotron/assets/stegs-low-poly.ply')
    # scene.add_object(cube)
    scene.add_object(model)
    tty_renderer = TTYRenderer()
    sdl_renderer = SDLRenderer(width=width, height=height)

    while True:
        t = time.time()
        cube.rotate(Vector3(t, t, t))
        model.rotate(Vector3(t, t, t))
        scene.update()
        tty_renderer.render(scene, draw_edges=False, draw_polys=True)
        sdl_renderer.render(scene, draw_edges=False, draw_polys=True)
