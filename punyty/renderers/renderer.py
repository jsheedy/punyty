import numpy as np


class Renderer():

    def __init__(self, *args, **kwargs):
        self.frame = 0

    def draw_line(self, points, color):
        raise NotImplementedError

    def clear(self):
        pass

    def prerender(self):
        pass

    def postrender(self):
        pass

    def draw_edges(self, points, edges):
        edges, color = edges
        for p1, p2 in edges:
            x1, y1 = points[p1]
            x2, y2 = points[p2]
            self.draw_line((x1, y1, x2, y2), color)

    def draw_vertices(self, verts):
        pass

    def draw_polys(self, points, polys):
        pass

    def render(self, scene, clear=True, draw_vertices=False, draw_polys=False):
        self.prerender()
        if clear:
            self.clear()
        self.frame += 1
        vertices = []
        edges = []
        polys = []
        n_points = 0
        for _name, obj in scene.objects.items():
            obj.update()
            obj_vertices = obj.transformed_vertices
            vertices.append(obj_vertices)
            # increment edge index
            obj_edges = [((edge[0]+n_points), (edge[1] + n_points)) for edge in obj.edges]
            edges.extend((obj_edges, obj.color))

            obj_polys = [((face[0]+n_points), (face[1] + n_points), (face[2] + n_points)) for face in obj.polys]
            polys.extend(obj_polys)

            n_points += obj_vertices.shape[1]

        vertices_matrix = np.hstack(vertices)
        points = self.vertices_to_screen(scene, vertices_matrix)

        points_list = points.T.tolist()
        if draw_vertices:
            self.draw_vertices(points_list)
        self.draw_edges(points_list, edges)
        if draw_polys:
            self.draw_polys(scene, vertices_matrix, points, polys)

        self.postrender()

    def vertices_to_screen(self, scene, vertices):
        transformed_vertices = scene.main_camera.R.I * scene.main_camera.T.I * vertices
        points = scene.main_camera.matrix() * transformed_vertices
        # perspective
        points = points[:2, :] / points[2, :]
        return points
