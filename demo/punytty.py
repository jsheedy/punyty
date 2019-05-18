import argparse
import os
import sys
import time

from punyty.model import Model
from punyty.objects import Cube, Octahedron
from punyty.renderers import TTYRenderer
from punyty.renderers.tty_renderer import ESC, RESET, HOME
from punyty.scene import Scene
from punyty.vector import Vector3
from demo import benchmark

BASEDIR = os.path.dirname(__file__)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--bunny',
        action='store_true',
        help='Stanford bunny'
    )

    parser.add_argument(
        '--polys',
        action='store_true',
        default=False,
        help='draw poly faces'
    )
    parser.add_argument(
        '--edges',
        action='store_true',
        default=True,
        help='draw vertex edges'
    )
    parser.add_argument(
        '--fps',
        action='store_true',
        default=False,
        help='print FPS'
    )
    return parser.parse_args()


def punytty():
    args = parse_args()
    scene = Scene()
    objects = []

    if args.bunny:
        path = os.path.join(BASEDIR, '../models/bunny.ply')
        bunny = Model.load_ply(path)
        bunny.position = Vector3(0,0,0)
        objects.append(bunny)
        args.polys = True
    else:
        objects.append(Octahedron(scale=Vector3(0.5, 0.5, 0.5), color=Vector3(1, 1, 1)))


    renderer = TTYRenderer(status_bar=args.fps)

    for o in objects:
        scene.add_object(o)

    bench = benchmark.Benchmark(renderer)
    fps = ''

    while True:
        t = time.time()
        for o in objects:
            o.rotate(Vector3(-.2, 0.5*t, t/10))
        renderer.render(scene, draw_polys=args.polys, draw_edges=(not args.polys))

        if args.fps:
            fps = bench.update(t) or fps
            sys.stdout.buffer.write(HOME + renderer.pixel(255, 255, 255) + fps.encode('utf8'))

if __name__ == '__main__':
    punytty()
