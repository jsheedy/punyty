import numpy as np

from .object3d import Object3D


def points_to_matrix(points):
    """ given a sequence of points, e.g. [(x1,y1,z1), ...]
    return them as homogenous coordinates (by adding a 4th dimension of
    value 1) in a column order np.matrix """
    points_matrix = np.matrix(points, dtype=np.float64).transpose()
    omega = np.ones(len(points), dtype=np.float64)
    points_matrix = np.matrix(np.vstack((points_matrix, omega)))
    return points_matrix


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
            normals = []
            centers = []

            for i in range(n_vertices):
                recs = f.readline().split()
                p = list(map(float, recs[:3]))
                vertices.append(p)

            for i in range(n_faces):
                recs = f.readline().split()
                p = tuple(map(int, recs))

                if p[0] == 3:  # triangles
                    triangle = p[1:]
                    obj.polys.append(triangle)

                if p[0] == 4:  # quadrilateral
                    triangle1 = p[1:4]
                    triangle2 = p[3:]
                    obj.polys.append(triangle1)
                    obj.polys.append(triangle2)

            obj.vertices = points_to_matrix(vertices)

            if ground:
                min_y = obj.vertices[1, :].min()
                obj.vertices[1, :] -= min_y / 2
            # centers, normals = obj.centers_and_normals()
            # obj.normals = points_to_matrix(normals)
            # obj.centers = points_to_matrix(centers)

            return obj
