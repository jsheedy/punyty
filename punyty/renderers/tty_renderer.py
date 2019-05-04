from functools import lru_cache
import logging
import shutil
import sys

import numpy as np

from .array_renderer import ArrayRenderer

logger = logging.getLogger(__name__)

ESC = b'\x1b['
RESET = ESC + b'0m'
HOME = ESC + b'1;1H'


class TTYRenderer(ArrayRenderer):
    """ renders to a tty """

    def __init__(self, status_bar=False, **kwargs):
        self.cols, self.rows = shutil.get_terminal_size()
        self.status_bar = status_bar
        if status_bar:
            self.rows = self.rows - 1

        self.target_array = np.zeros((self.rows, self.cols, 3))
        super().__init__(target_array=self.target_array, **kwargs)

    @lru_cache(maxsize=None)
    def pixel(self, r=0, g=255, b=0):
        block = '█'.encode('utf8')
        if r == 0 and g == 0 and b == 0:
            return b' '  #block
        return ESC + b'38;2;' + f'{r};{g};{b}'.encode('utf8') + b'm' + block


    def postrender(self):
        colors = (255 * self.target_array).astype(np.uint8)
        l = colors.reshape(self.cols*self.rows, 3)
        s = b''.join(map(lambda c: self.pixel(r=c[0], g=c[1], b=c[2]), l))
        if self.status_bar:
            home = ESC + b'2;1H'
        else:
            home = HOME
        sys.stdout.buffer.write(home + s)
