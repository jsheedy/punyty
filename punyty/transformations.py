from math import sin, cos
import numpy as np

from .vector import Vector3

def rotation_matrix(rotation=None):
    r = rotation or Vector3()
    rot_x = np.matrix([
        [1, 0, 0, 0],
        [0, cos(r.x), -sin(r.x), 0],
        [0, sin(r.x), cos(r.x), 0],
        [0, 0, 0, 1]
    ], dtype=np.float64)

    rot_y = np.matrix([
        [cos(r.y), 0, sin(r.y), 0],
        [0, 1, 0, 0],
        [-sin(r.y), 0, cos(r.y), 0],
        [0, 0, 0, 1]
    ], dtype=np.float64)

    rot_z = np.matrix([
        [cos(r.z), -sin(r.z), 0, 0],
        [sin(r.z), cos(r.z), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=np.float64)

    return rot_z * rot_x * rot_y

def scale_matrix(scale=None):

    s = scale or Vector3.unity()

    return np.matrix([
        [s.x, 0, 0, 0],
        [0, s.y, 0, 0],
        [0, 0, s.z, 0],
        [0, 0, 0, 1]
    ],dtype=np.float64)

def translation_matrix(t=None):
    t = t or Vector3()
    return np.matrix([
        [1, 0, 0, t.x],
        [0, 1, 0, t.y],
        [0, 0, 1, t.z],
        [0, 0, 0, 1]
    ], dtype=np.float64)

