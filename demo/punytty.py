import time

from punyty.model import Model
from punyty.objects import Cube
from punyty.renderers import TTYRenderer
from punyty.scene import Scene
from punyty.vector import Vector3


def punytty():
    scene = Scene()
    cube = Cube(color=(1, 0, 1))
    scene.add_object(cube)
    renderer = TTYRenderer()
    # bunny = Model.load_ply('models/bunny.ply')
    # bunny.position = Vector3(0,0,-6)
    # scene.add_object(bunny)
    while True:
        cube.rotate(Vector3(time.time(), 0.5*time.time(), 0.1*time.time()))
        renderer.render(scene, draw_polys=True, draw_edges=False)

if __name__ == '__main__':
    punytty()
