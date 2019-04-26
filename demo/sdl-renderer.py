import time

from punyty.vector import Vector3
from punyty.objects import Cube
from punyty.renderers import SDLRenderer
from punyty.scene import Scene


if __name__ == '__main__':
    width = height = 800

    scene = Scene(f=2000, cx=width/2, cy=height/2)
    cube = Cube(color=(0, 1, 1))
    scene.add_object(cube)
    renderer = SDLRenderer(width=width, height=height)

    while True:
        t = time.time()
        renderer.render(scene, draw_polys=True)
        cube.rotate(Vector3(t, t, 0))
