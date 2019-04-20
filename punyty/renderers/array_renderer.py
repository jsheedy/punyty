import logging

import numpy as np
from skimage.draw import line_aa, line

from .renderer import Renderer
from .. import geom

logger = logging.getLogger(__name__)


class ArrayRenderer(Renderer):
    """ renders to a numpy array """

    def __init__(self,  *args, target_array=None, **kwargs):
        super().__init__(*args, **kwargs)
        h, w = target_array.shape[:2]
        self.width = w
        self.height = h
        self.target_array = target_array

    def clear(self):
        self.target_array[::] = 0.0

    def draw_line(self, rgb, pts):
        # from biofeedbackcube.buffer
        assert len(pts) == 4
        # if points lie outside uv, find the intersection points
        intersections = geom.line_intersects_uv(*pts)
        if len(intersections) == 2:
            x0, y0 = intersections[0]
            x1, y1 = intersections[1]
        elif len(intersections) == 1:
            x0, y0 = intersections[0]
            if geom.point_in_uv(*pts[:2]):
                x1, y1 = pts[:2]
            elif geom.point_in_uv(*pts[2:]):
                x1, y1 = pts[2:]
            else:
                return
        elif geom.point_in_uv(*pts[:2]) and geom.point_in_uv(*pts[2:]):
            x0, y0, x1, y1 = pts
        else:
            return

        ix0 = int(x0 * (self.width-1))
        iy0 = int(y0 * (self.height-1))
        ix1 = int(x1 * (self.width-1))
        iy1 = int(y1 * (self.height-1))
        rr, cc, val = line_aa(ix0, iy0, ix1, iy1)
        r,g,b = rgb
        # import pdb;pdb.set_trace()
        self.target_array[cc, rr, 0] += val * r
        self.target_array[cc, rr, 1] += val * g
        self.target_array[cc, rr, 2] += val * b

    def draw_edges(self, points, edges, color=(0,1,0)):
        for p1, p2 in edges:
            x1, y1 = points[p1]
            x2, y2 = points[p2]
            self.draw_line(color, (x1, y1, x2, y2))
