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
    # scene.add_object(cube)
    bunny = Model.load_ply('models/bunny.ply')
    bunny.position = Vector3(0,-.1,-4)
    scene.add_object(bunny)
    renderer = SDLRenderer(width=width, height=height)

    i = 0
    t0 = time.time()
    n_frames = 200
    while True:
        i += 1
        t = time.time()
        renderer.render(scene, draw_edges=False, draw_polys=True, draw_axes=False)
        bunny.rotate(Vector3(t/2, t/1, t/3))
        cube.rotate(Vector3(t, t/1, t))
        if i % n_frames == 0:
            dt = t - t0
            t0 = time.time()
            fps = n_frames / dt
            print(f'fps: {fps:.2f}')

        # time.sleep(0.005)
