from functools import lru_cache
import logging
import shutil
import sys

import numpy as np

from .array_renderer import ArrayRenderer

logger = logging.getLogger(__name__)

ESC = b'\x1b['
RESET = ESC + b'0m'
HOME = ESC + b'0;0H'


class TTYRenderer(ArrayRenderer):
    """ renders to a tty """

    def __init__(self):
        self.cols, self.rows = shutil.get_terminal_size()
        self.target_array = np.zeros((self.rows, self.cols, 3))
        super().__init__(target_array=self.target_array)

    @lru_cache()
    def pixel(self, color=(0, 255, 0)):
        block = '█'.encode('utf8')
        r, g, b = color
        return ESC + b'38;2;' + f'{r};{g};{b}'.encode('utf8') + b'm' + block

    def render(self, scene, **kwargs):
        super().render(scene, **kwargs)
        sys.stdout.buffer.write(HOME)
        colors = (255 * self.target_array).astype(np.uint8)
        for r in range(self.rows):
            for c in range(self.cols):
                color = tuple(colors[r, c, :])
                p = self.pixel(color=color)
                sys.stdout.buffer.write(p)
