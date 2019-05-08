import numpy as np


class Renderer():

    def __init__(self, *args, **kwargs):
        self.frame = 0

    def draw_line(self, points, color):
        raise NotImplementedError

    def draw_axes(self, scene):
        pass

    def clear(self):
        pass

    def prerender(self):
        pass

    def postrender(self):
        pass

    def draw_edges(self, points, edges, colors):
        for i, obj_edges in enumerate(edges):
            color = colors[i]
            for p1, p2 in obj_edges:
                x1 = points[0, p1]
                x2 = points[0, p2]
                y1 = points[1, p1]
                y2 = points[1, p2]
                self.draw_line((x1, y1, x2, y2), color)

    def draw_vertices(self, verts):
        pass

    def draw_poly(self, x1, y1, x2, y2, x3, y3, color):
        pass

    def draw_polys(self, scene, normals, centers, points, polys, colors):
        light_vector = scene.main_light.direction
        light_dot_products = np.dot(light_vector, normals[:3, :])
        camera_dot_products = np.dot(scene.main_camera.position.normalize().A, normals[:3, :])

        camera_vector = np.expand_dims(scene.main_camera.position.A, 1) - centers[:3, :]
        distance = np.linalg.norm(camera_vector, axis=0)

        eligible_polys = (camera_dot_products > 0.0) & (light_dot_products > 0)
        forward_polys = np.arange(len(polys), dtype=np.uint32)[eligible_polys]
        depth_coords = [(distance[i], i) for i in forward_polys]
        depth_coords.sort(reverse=True)
        for _, i in depth_coords:
            l = light_dot_products[i]
            p1, p2, p3 = polys[i]
            x1, y1 = points[0, p1], points[1, p1]
            x2, y2 = points[0, p2], points[1, p2]
            x3, y3 = points[0, p3], points[1, p3]

            lit_color = tuple(map(lambda x: x * l, colors[i]))
            self.draw_poly(x1, y1, x2, y2, x3, y3, lit_color)


    def render(self, scene,
                    clear=True,
                    draw_edges=True,
                    draw_polys=False,
                    draw_axes=False):

        self.prerender()
        if clear:
            self.clear()
        self.frame += 1

        vertices = []
        normals = []
        centers = []
        edges = []
        polys = []
        colors = []
        n_points = 0
        for _, obj in scene.objects.items():
            obj.update()
            vertices.append(obj.transformed_vertices)
            normals.append(obj.transformed_normals)
            centers.append(obj.transformed_centers)
            if obj.edges:
                obj_edges = [((edge[0]+n_points), (edge[1] + n_points)) for edge in obj.edges]
                edges.append(obj_edges)

            obj_polys = [((poly[0]+n_points), (poly[1] + n_points), (poly[2] + n_points)) for poly in obj.polys]
            colors.extend([obj.color for _ in obj.polys])
            polys.extend(obj_polys)

            n_points += obj.vertices.shape[1]

        vertices_matrix = np.hstack(vertices)
        normals_matrix = np.hstack(normals)
        centers_matrix = np.hstack(centers)

        points = self.vertices_to_screen(scene, vertices_matrix)

        if edges and draw_edges:
            self.draw_edges(points, edges, colors)
        if draw_polys:
            self.draw_polys(scene, normals_matrix, centers_matrix, points, polys, colors)
        if draw_axes:
            self.draw_axes(scene)

        self.postrender()

    def vertices_to_screen(self, scene, vertices):
        transformed_vertices = np.linalg.inv(scene.main_camera.R) @ np.linalg.inv(scene.main_camera.T) @ vertices
        points = scene.main_camera.matrix() @ transformed_vertices
        # perspective
        points = points[:2, :] / points[2, :]
        return points
