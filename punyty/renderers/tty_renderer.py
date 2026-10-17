import shutil
import sys

import numpy as np

from .array_renderer import ArrayRenderer


ESC = b'\x1b['
RESET = ESC + b'0m'
HOME = ESC + b'1;1H'
BLOCK = '█'.encode('utf8')
RGB_MODE = b'38;2;'

class TTYRenderer(ArrayRenderer):
    """ renders to a tty """

    def __init__(self, status_bar=False, **kwargs):
        self.cols, self.rows = shutil.get_terminal_size()
        self.status_bar = status_bar
        if status_bar:
            self.rows = self.rows - 1

        self.target_array = np.zeros((self.rows, self.cols, 3), dtype=np.float32)
        self.int_to_bytes_map = {
            i: str(i).encode('utf8')
            for i in range(256)
        }
        super().__init__(target_array=self.target_array, pixel_aspect=1.5, **kwargs)


    def pixel(self, color):
        return (
            ESC
            + RGB_MODE
            + self.int_to_bytes_map[color[0]]
            + b';'
            + self.int_to_bytes_map[color[1]]
            + b';'
            + self.int_to_bytes_map[color[2]]
            + b'm'
            + BLOCK
        )


    def postrender(self):
        colors = (255 * self.target_array).astype(np.uint8)
        l = colors.reshape(-1, 3)
        s = b''.join(map(self.pixel, l))
        if self.status_bar:
            home = ESC + b'2;1H'
        else:
            home = HOME
        sys.stdout.buffer.write(home + s)
