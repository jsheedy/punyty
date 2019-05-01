import time

from punyty.vector import Vector3
from punyty.objects import Cube
from punyty.model import Model
from punyty.renderers import SDLRenderer
from punyty.scene import Scene


if __name__ == '__main__':
    width = height = 800

    scene = Scene(f=2000, cx=width/2, cy=height/2)
    cube = Cube(color=(0, 1, 1))
    scene.add_object(cube)
    # bunny = Model.load_ply('models/bunny.ply')
    # bunny.position = Vector3(0,0,-4)
    # scene.add_object(bunny)
    renderer = SDLRenderer(width=width, height=height)

    while True:
        t = time.time()
        renderer.render(scene, draw_polys=True, draw_axes=False)
        # bunny.rotate(Vector3(0, t/1, 0))
        cube.rotate(Vector3(t, t/1, t))
