import numpy as np

from .object3d import Object3D


class Model(Object3D):

    @classmethod
    def load_ply(cls, fname, position=None, scale=None, rotation=None):

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
                    obj.polys.append(triangle)  # <-- change winding order

                if p[0] == 4:  # quadrilateral
                    triangle1 = p[1:4][::-1]
                    triangle2 = p[3:][::-1]
                    obj.polys.append(triangle1)
                    obj.polys.append(triangle2)

            obj.vertices = np.array(vertices)

            # center it
            obj.vertices -= np.mean(obj.vertices, axis=0)

        obj.__init__()

        return obj
