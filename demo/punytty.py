import argparse
import sys
import time
from pathlib import Path

from punyty.model import Model
from punyty.objects import Cube
from punyty.renderers import TTYRenderer
from punyty.renderers.tty_renderer import HOME
from punyty.scene import Scene
from punyty.vector import Vector3
from demo import benchmark

BASEDIR = Path(__file__).parent


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
        default=True,
        help='draw poly faces'
    )
    parser.add_argument(
        '--edges',
        action='store_true',
        default=False,
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

    if args.bunny:
        path = BASEDIR / '../punyty/models/bunny.ply'
        object = Model.load_ply(path)
    else:
        object = Cube(color=Vector3(.1, 1, .2))
        object.position = Vector3(0.0, 0.0, 5.0)

    scene.add_object(object)

    renderer = TTYRenderer(
        status_bar=args.fps,
        draw_polys=args.polys,
        draw_edges=(not args.polys)
    )

    bench = benchmark.Benchmark(renderer)
    fps = ''

    while True:
        t = time.time()
        scene.update()
        object.rotate(Vector3(-.2, 0.5*t, t/10))
        renderer.render(scene)

        if args.fps:
            fps = bench.update(t) or fps
            sys.stdout.buffer.write(HOME + renderer.pixel([255, 255, 255]) + fps.encode('utf8'))


if __name__ == '__main__':
    punytty()
