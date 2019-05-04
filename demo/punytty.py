import argparse
import os
import time

from punyty.model import Model
from punyty.objects import Cube
from punyty.renderers import TTYRenderer
from punyty.scene import Scene
from punyty.vector import Vector3


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
    return parser.parse_args()


def punytty():
    args = parse_args()
    scene = Scene()
    objects = []

    if args.bunny:
        path = os.path.join(BASEDIR, '../models/bunny.ply')
        bunny = Model.load_ply(path)
        bunny.position = Vector3(.02,-.12,-4.5)
        objects.append(bunny)
        args.polys = True
    else:
        objects.append(Cube(color=(0, 1, 0)))


    renderer = TTYRenderer()

    for o in objects:
        scene.add_object(o)

    while True:
        for o in objects:
            o.rotate(Vector3(-.2, 0.5*time.time(), 0))
        renderer.render(scene, draw_polys=args.polys, draw_edges=(not args.polys))

if __name__ == '__main__':
    punytty()
