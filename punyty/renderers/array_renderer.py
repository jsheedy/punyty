import logging

import numpy as np
from skimage.draw import line_aa

from .renderer import Renderer
from .. import geom

logger = logging.getLogger(__name__)


class ArrayRenderer(Renderer):
    """ renders to a numpy array """

    def __init__(self, target_array, f=3.0, window_title="punyty"):
        h, w = target_array.shape[:2]
        self.width = w
        self.height = h
        self.f = f
        self.frame = 0
        self.target_array = target_array

    def vertices_to_screen(self, scene, vertices):
        camera_matrix = self.camera_matrix()
        transformed_vertices = scene.main_camera.R.I * scene.main_camera.T.I * vertices

        points = camera_matrix * transformed_vertices
        # perspective
        points = points[:2, :] / points[2, :]
        return points

    def draw_line(self, rgb, pts):
        # from biofeedbackcube.buffer
        assert len(pts) == 4
        # if points lie outside uv, find the intersection points
        intersections = geom.line_intersects_uv(*pts)
        if len(intersections) == 2:
            x0, y0 = intersections[0]
            x1, y1 = intersections[1]
        elif len(intersections) == 1:
            x0, y0 = intersections[0]
            if geom.point_in_uv(*pts[:2]):
                x1, y1 = pts[:2]
            elif geom.point_in_uv(*pts[2:]):
                x1, y1 = pts[2:]
            else:
                return
        elif geom.point_in_uv(*pts[:2]) and geom.point_in_uv(*pts[2:]):
            x0, y0, x1, y1 = pts
        else:
            return

        ix0 = int(x0 * (self.width-1))
        iy0 = int(y0 * (self.height-1))
        ix1 = int(x1 * (self.width-1))
        iy1 = int(y1 * (self.height-1))
        rr, cc, val = line_aa(ix0, iy0, ix1, iy1)
        r,g,b = rgb
        self.target_array[rr, cc, 0] += r * val
        self.target_array[rr, cc, 1] += g * val
        self.target_array[rr, cc, 2] += b * val

    def draw_edges(self, points, edges, color=(0,1,0)):
        for p1, p2 in edges:
            x1, y1 = points[p1]
            x2, y2 = points[p2]
            self.draw_line(color, (x1, y1, x2, y2))

    def render(self, scene, **kwargs):
        self.frame += 1
        vertices = []
        edges = []
        n_points = 0
        for name, obj in scene.objects.items():
            obj.update()
            obj_vertices = obj.transformed_vertices
            vertices.append(obj_vertices)
            # increment edge index
            obj_edges = [((edge[0]+n_points), (edge[1] + n_points)) for edge in obj.edges]
            edges.extend(obj_edges)
            n_points += obj_vertices.shape[1]

        vertices_matrix = np.hstack(vertices)
        points = self.vertices_to_screen(scene, vertices_matrix)

        points_list = points.T.tolist()
        self.draw_edges(points_list, edges)

    def camera_matrix(self):
        cx = 0.5
        cy = 0.5
        f = self.f

        return np.matrix([
            [f, 0, cx, 0],
            [0, -f, cy, 0],
            [0, 0, 1, 0]
        ], dtype=np.float64)
