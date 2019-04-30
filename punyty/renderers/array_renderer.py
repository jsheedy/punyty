import logging

from skimage.draw import line_aa
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
        self.target_array[::] = 0.0

    def draw_line(self, points, color):
        x0, y0, x1, y1 = points
        ix0 = int(x0 * (self.width-1))
        iy0 = int(y0 * (self.height-1))
        ix1 = int(x1 * (self.width-1))
        iy1 = int(y1 * (self.height-1))
        rr, cc, val = line_aa(ix0, iy0, ix1, iy1)
        r, g, b = color
        mask = (rr >= 0) & (rr < self.width) & (cc >= 0) & (cc < self.height)
        ccm = cc[mask]
        rrm = rr[mask]
        valm = val[mask]
        self.target_array[ccm, rrm, 0] += valm * r
        self.target_array[ccm, rrm, 1] += valm * g
        self.target_array[ccm, rrm, 2] += valm * b

    def draw_poly(self, x1, y1, x2, y2, x3, y3, color):
        rows = tuple(map(lambda x: x*(self.height-1), (y1, y2, y3)))
        cols = tuple(map(lambda x: x*(self.width-1), (x1, x2, x3)))

        r, g, b = color
        rr, cc = polygon(cols, rows, shape=None)
        mask = (rr >= 0) & (rr < self.width) & (cc >= 0) & (cc < self.height)
        ccm = cc[mask]
        rrm = rr[mask]
        self.target_array[ccm, rrm, 0] += r
        self.target_array[ccm, rrm, 1] += g
        self.target_array[ccm, rrm, 2] += b