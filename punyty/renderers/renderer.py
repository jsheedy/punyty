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

    def draw_poly(self, x1, y1, x2, y2, x3, y3, color):
        pass

    def draw_polys(self, scene, vertices, normals, points, polys, color=(0, 1.0, 0)):

        # light_vector = scene.main_light.position.A - np.mean(poly_coords.A, axis=2)
        # light_vector = light_vector / np.expand_dims(np.linalg.norm(light_vector, axis=1), 2)

        light_vector = np.array([0, 0, -1])
        dot_products = light_vector * normals[:3, :]  # ).sum(axis=1)
        for i, (p1, p2, p3) in enumerate(polys):

            x1, y1 = points[0, p1], points[1, p1]
            x2, y2 = points[0, p2], points[1, p2]
            x3, y3 = points[0, p3], points[1, p3]

            l = dot_products[0, i]

            if l > 0:
                lighted_color = tuple(map(lambda x: x * l, color))
                self.draw_poly(x1, y1, x2, y2, x3, y3, lighted_color)

    def render(self, scene,
                    clear=True,
                    draw_edges=True,
                    draw_vertices=False,
                    draw_polys=False,
                    draw_axes=False):

        self.prerender()
        if clear:
            self.clear()
        self.frame += 1
        vertices = []
        normals = []
        edges = []
        polys = []
        n_points = 0
        for _name, obj in scene.objects.items():
            obj.update()
            obj_vertices = obj.transformed_vertices
            obj_normals = obj.transformed_normals
            vertices.append(obj_vertices)
            normals.append(obj_normals)
            if obj.edges:
                obj_edges = [((edge[0]+n_points), (edge[1] + n_points)) for edge in obj.edges]
                edges.extend((obj_edges, obj.color))

            obj_polys = [((face[0]+n_points), (face[1] + n_points), (face[2] + n_points)) for face in obj.polys]
            polys.extend(obj_polys)

            n_points += obj_vertices.shape[1]

        vertices_matrix = np.hstack(vertices)
        normals_matrix = np.hstack(normals)

        points = self.vertices_to_screen(scene, vertices_matrix)

        points_list = points.T.tolist()
        if draw_vertices:
            self.draw_vertices(points_list)
        if edges and draw_edges:
            self.draw_edges(points_list, edges)
        if draw_polys:
            self.draw_polys(scene, vertices_matrix, normals_matrix, points, polys)
        if draw_axes:
            self.draw_axes(scene)
        self.postrender()

    def vertices_to_screen(self, scene, vertices):
        transformed_vertices = scene.main_camera.R.I * scene.main_camera.T.I * vertices
        points = scene.main_camera.matrix() * transformed_vertices
        # perspective
        points = points[:2, :] / points[2, :]
        return points
