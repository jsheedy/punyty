from datetime import datetime

import numpy as np

from .transformations import rotation_matrix, scale_matrix, translation_matrix
from .vector import Vector3, ZeroVectorError


class Object3D:
    vertices = ()
    edges = ()
    polys = ()
    normals = ()
    centers = ()

    def __init__(self, position=None, angular_velocity=None, velocity=None, scale=None, rotation=None, color=(0, 1, 0)):
        self.position = position or Vector3()
        self.update_time = datetime.now()
        self.velocity = velocity
        self.angular_velocity = angular_velocity
        self._translation_matrix = translation_matrix(position or Vector3.zero())
        self._scale_matrix = scale_matrix(scale or Vector3.unity())
        self._rotation_matrix = rotation_matrix(rotation)
        self.color = color
        if (not self.normals) and self.polys:
            self.normals = self.to_homogenous_coords(self.calculate_normals())
        if (not self.centers) and self.polys:
            self.centers = self.calculate_centers()
        if len(self.vertices):
            self.vertices = self.to_homogenous_coords(self.vertices / 2)


    def calculate_normals(self):
        polys = np.array(self.polys, dtype=np.uint32)
        poly_coords = self.vertices[polys]
        p0 = poly_coords[:, 0::3, :].squeeze()
        p1 = poly_coords[:, 1::3, :].squeeze()
        p2 = poly_coords[:, 2::3, :].squeeze()
        l1 = p1 - p0
        l2 = p2 - p1
        cross = np.cross(l2, l1, axis=1)
        return cross / np.expand_dims(np.linalg.norm(cross, axis=1), 2)

    def calculate_centers(self):
        polys = np.array(self.polys, dtype=np.uint32)
        poly_coords = np.array(self.vertices)[polys]
        centers = np.mean(poly_coords, axis=2)
        return self.to_homogenous_coords(centers)

    def update(self):
        self.update_physics()

    def update_physics(self):
        if not self.velocity:
            return
        t1 = datetime.now()
        time_dot_delta_time = (t1 - self.update_time).total_seconds()
        self.update_time = t1
        self.position += self.velocity * time_dot_delta_time
        # FIXME: implement angular velocity
        # self.rotation += self.angular_velocity * time_dot_delta_time

    def to_homogenous_coords(self, vertices):
        return np.vstack([vertices.T, np.ones(vertices.shape[0]).T])

    @property
    def position(self):
        return Vector3(*self.T[:3, 3])

    @position.setter
    def position(self, v):
        self._translation_matrix = translation_matrix(v)

    @property
    def scale(self):
        return Vector3(*self.S[:3, 3])

    @scale.setter
    def scale(self, scale):
        self._scale_matrix = scale_matrix(Vector3(scale, scale, scale))

    @property
    def T(self):
        return self._translation_matrix

    @property
    def R(self):
        return self._rotation_matrix

    @property
    def S(self):
        return self._scale_matrix

    @property
    def transformed_vertices(self):
        return self.T @ self.R @ self.S @ self.vertices

    @property
    def transformed_normals(self):
        return self.T @ self.R @ self.S @ self.normals

    @property
    def transformed_centers(self):
        return self.T @ self.R @ self.S @ self.centers

    def look_at(self, target, up=None):
        """ aims camera at target, with specified up vector, or world up.
        Does nothing if target is coincident """

        if target == self.position:
            raise Exception("can't look at self")

        z_axis = (target - self.position).normalize()

        if up:
            up = up.normalize()
        else:
            up = Vector3(0, 1, 0)

        try:
            x_axis = -up.cross(z_axis).normalize()
        except ZeroVectorError:
            left = Vector3(-1, 0, 0)
            x_axis = left.cross(z_axis).normalize()

        y_axis = -z_axis.cross(x_axis)

        self._rotation_matrix = np.array([
            [x_axis.x, y_axis.x, z_axis.x, 0],
            [x_axis.y, y_axis.y, z_axis.y, 0],
            [x_axis.z, y_axis.z, z_axis.z, 0],
            [0, 0, 0, 1]
        ], dtype=np.float64)

    def rotate(self, vector):
        self._rotation_matrix = rotation_matrix(vector)
