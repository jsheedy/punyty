import time

from punyty.vector import Vector3
from punyty.objects import Cube
from punyty.renderers import TTYRenderer
from punyty.scene import Scene


if __name__ == '__main__':

    scene = Scene()
    cube = Cube()
    scene.add_object(cube)
    renderer = TTYRenderer()
    while True:
        cube.rotate(Vector3(time.time(), 0.5*time.time(), 0.1*time.time()))
        renderer.render(scene)
