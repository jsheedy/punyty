import numpy as np

from .object3d import Object3D


class Camera(Object3D):
    def __init__(self, f=3.0, cx=0.5, cy=0.5, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.f = f
        self.cx = cx
        self.cy = cy

    def matrix(self):
        cx = self.cx
        cy = self.cy
        f = self.f

        return np.array([
            [f, 0, cx, 0],
            [0, -f, cy, 0],
            [0, 0, 1, 0]
        ], dtype=np.float64)
