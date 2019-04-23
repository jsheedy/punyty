from datetime import datetime

import numpy as np

from .transformations import rotation_matrix, scale_matrix, translation_matrix
from .vector import Vector3, ZeroVectorError


class Object3D:
    vertices = ()
    edges = ()

    def __init__(self, position=None, angular_velocity=None, velocity=None, scale=None, rotation=None, color=(0, 1, 0)):
        self._translation_matrix = translation_matrix(position or Vector3())
        self.update_time = datetime.now()
        self.velocity = velocity
        self.angular_velocity = angular_velocity
        self._scale_matrix = scale_matrix(scale or Vector3.unity())
        self._rotation_matrix = rotation_matrix(rotation)
        self.color = color

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
        return np.hstack([vertices, np.matrix(np.ones(vertices.shape[0])).T]).T

    @property
    def position(self):
        return Vector3(*self.T[:3,3])

    @position.setter
    def position(self, v):
        self._translation_matrix = translation_matrix(v)

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
        return self.T * self.R * self.S * self.vertices

    def set_scale(self, scale):
        self._scale_matrix = scale_matrix(Vector3(scale, scale, scale))

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

        self._rotation_matrix = np.matrix([
            [x_axis.x, y_axis.x, z_axis.x, 0],
            [x_axis.y, y_axis.y, z_axis.y, 0],
            [x_axis.z, y_axis.z, z_axis.z, 0],
            [0, 0, 0, 1]
        ], dtype=np.float64)

    def rotate(self, vector):
        self._rotation_matrix = rotation_matrix(vector)