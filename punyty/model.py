import numpy as np

from .object3d import Object3D


class Model(Object3D):

    @classmethod
    def load_ply(cls, fname, ground=True, position=None, scale=None, rotation=None):

        obj = cls(position=position, scale=scale, rotation=rotation)

        with open(fname) as f:

            for line in (x.strip() for x in f):
                if line == "end_header":
                    break
                if "element vertex" in line:
                    n_vertices = int(line.split()[2])
                if "element face" in line:
                    n_faces = int(line.split()[2])

            vertices = []
            obj.polys = []

            for _ in range(n_vertices):
                recs = f.readline().split()
                p = list(map(float, recs[:3]))
                vertices.append(p)

            for _ in range(n_faces):
                recs = f.readline().split()
                p = tuple(map(int, recs))

                if p[0] == 3:  # triangles
                    triangle = p[1:]
                    obj.polys.append(triangle[::-1])  # <-- change winding order

                if p[0] == 4:  # quadrilateral
                    triangle1 = p[1:4][::-1]
                    triangle2 = p[3:][::-1]
                    obj.polys.append(triangle1)
                    obj.polys.append(triangle2)

            obj.vertices = np.array(vertices)

            if ground:
                min_y = obj.vertices[1, :].min()
                obj.vertices[1, :] -= min_y / 2

            obj.__init__()
            obj.vertices = obj.to_homogenous_coords(obj.vertices)

            return obj
