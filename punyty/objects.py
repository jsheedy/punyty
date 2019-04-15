from math import sqrt
import numpy as np

from .object3d import Object3D


class Cube(Object3D):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        vertices = np.matrix([
            [1, 1, -1],
            [-1, 1, -1],
            [-1, -1, -1],
            [1, -1, -1],

            [1, 1, 1],
            [-1, 1, 1],
            [-1, -1, 1],
            [1, -1, 1]
        ], dtype=np.float64)
        self.vertices = self.to_homogenous_coords(vertices / 2)

        self.edges = (
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),

            (4, 5),
            (5, 6),
            (6, 7),
            (7, 4),

            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7),
        )

        self.polys = (
            (0, 1, 2),
            (2, 3, 0),
            (4, 7, 6),
            (6, 5, 4),
            (1, 5, 6),
            (6, 2, 1),
            (0, 3, 7),
            (7, 4, 0),
            (3, 2, 6),
            (6, 7, 3),
            (5, 1, 0),
            (0, 4, 5),
        )


class Tetrahedron(Object3D):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        vertices = np.matrix([
            [1, 1, 1],
            [-1, -1, 1],
            [1, -1, -1],
            [-1, 1, -1],
        ], dtype=np.float64)

        self.edges = (
            (0, 1),
            (1, 2),
            (2, 3),
            (1, 3),
            (0, 2),
            (0, 3),
        )
        self.vertices = self.to_homogenous_coords(vertices / 2)


class Octahedron(Object3D):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        vertices = np.matrix([
            [1, 0, 0],
            [-1, 0, 0],
            [0, 1, 0],
            [0, -1, 0],
            [0, 0, 1],
            [0, 0, -1],
        ], dtype=np.float64)

        self.edges = (
            (0, 2),
            (0, 3),
            (0, 4),
            (0, 5),

            (1, 2),
            (1, 3),
            (1, 4),
            (1, 5),

            (2, 4),
            (2, 5),
            (3, 4),
            (3, 5),
        )
        self.vertices = self.to_homogenous_coords(vertices / 2)


class Dodecahedron(Object3D):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # lay out as cube + 3 rects as on
        # https://en.wikipedia.org/wiki/Regular_dodecahedron?oldformat=true#Cartesian_coordinates
        phi = (1 + sqrt(5)) / 2

        vertices = np.matrix([
            # cube
            [1, 1, 1], # 0
            [1, -1, 1],
            [-1, -1, 1],
            [-1, 1, 1],

            [1, 1, -1], # 3
            [1, -1, -1],
            [-1, -1, -1],
            [-1, 1, -1],

            # red/pink rectangle (xy)
            [phi, 1/phi, 0], # 8
            [phi, -1/phi, 0],
            [-phi, -1/phi, 0],
            [-phi, 1/phi, 0],

            #green rectangle (yz)
            [0, phi, 1/phi],  #12
            [0, phi, -1/phi],
            [0, -phi, -1/phi],
            [0, -phi, 1/phi],

            # blue rectangle (xz)
            [1/phi, 0, phi], # 16
            [1/phi, 0, -phi],
            [-1/phi, 0, -phi],
            [-1/phi, 0, phi]

        ], dtype=np.float64)

        self.edges = (
            # one r/g/b vertex for each cube corner vertex
            (0, 8),
            (0, 12),
            (0, 16),

            (1, 9),
            (1, 15),
            (1, 16),

            (2, 10),
            (2, 15),
            (2, 19),

            (3, 11),
            (3, 12),
            (3, 19),

            (4, 8),
            (4, 13),
            (4, 17),

            (5, 9),
            (5, 14),
            (5, 17),

            (6, 10),
            (6, 14),
            (6, 18),

            (7, 11),
            (7, 13),
            (7, 18),

            # lace up the rects exterior edges
            # r
            (8, 9),
            (10, 11),
            # g
            (12, 13),
            (14, 15),
            # b
            (17, 18),
            (19, 16)
        )
        self.vertices = self.to_homogenous_coords(vertices / (2*phi))
