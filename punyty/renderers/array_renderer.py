import logging

import numpy as np
from skimage.draw import line_aa, line
from skimage.draw import polygon

from .renderer import Renderer

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
        self.target_array[...] = 0.0

    def draw_line(self, points, color):
        rr, cc, val = line_aa(*points)
        mask = (rr >= 0) & (rr < self.width) & (cc >= 0) & (cc < self.height)
        ccm = cc[mask]
        rrm = rr[mask]
        valm = val[mask]
        self.target_array[ccm, rrm] += ((np.vstack((valm, valm, valm)).T * np.array(color)))
        # non-aa line:
        # rr, cc = line(ix0, iy0, ix1, iy1)
        # self.target_array[ccm, rrm] += np.array(color)

    def draw_poly(self, x1, y1, x2, y2, x3, y3, color):
        rows = y1, y2, y3
        cols = x1, x2, x3
        rr, cc = polygon(cols, rows)
        mask = (rr >= 0) & (rr < self.width) & (cc >= 0) & (cc < self.height)
        ccm = cc[mask]
        rrm = rr[mask]
        self.target_array[ccm, rrm] = color
