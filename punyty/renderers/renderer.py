import numpy as np

from punyty.scene import DirectionalLight, PointLight, AmbientLight


class Renderer():

    def __init__(
            self,
            *args,
            pixel_aspect=1.0,
            max_depth=1000,
            min_depth=0.1,
            clear=True,
            draw_edges=True,
            draw_wireframe=False,
            draw_polys=True,
            draw_axes=False,
            draw_centers=False,
            **kwargs):

        self.frame = 0
        self.max_depth = max_depth
        self.min_depth = min_depth
        self.width = 1
        self.height = 1
        self.pixel_aspect = pixel_aspect
        self._clear = clear
        self._draw_edges = draw_edges
        self._draw_wireframe = draw_wireframe
        self._draw_polys = draw_polys
        self._draw_axes = draw_axes
        self._draw_centers = draw_centers

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

    def draw_centers(self, centers):
        pass

    def draw_poly(self, x1, y1, x2, y2, x3, y3, color):
        pass

    def draw_wireframe(self, points, polys, colors):

        for i, (p1, p2, p3) in enumerate(polys):
            # p1, p2, p3 = polys[i]
            color = colors[i]
            x1, y1 = points[0, p1], points[1, p1]
            x2, y2 = points[0, p2], points[1, p2]
            x3, y3 = points[0, p3], points[1, p3]
            self.draw_line((x1, y1, x2, y2), color)
            self.draw_line((x2, y2, x3, y3), color)
            self.draw_line((x3, y3, x1, y1), color)

    def draw_polys(self, scene, normals, centers, points, polys, colors):
        forward = scene.main_camera.forward[:3]

        camera_vector = centers[:3, :] - np.expand_dims(scene.main_camera.position.A, 1)
        distance = np.linalg.norm(camera_vector, axis=0)
        camera_normals = camera_vector / distance
        camera_dot_products = np.dot(forward, camera_normals)

        cone_of_vision_mask = camera_dot_products > 0.95  # 0.95 is sweet spot for sdl renderer #self.joystick.x
        distance_mask = (distance < self.max_depth) & (distance > self.min_depth)
        front_facing_mask = np.dot(-1*forward, normals[:3, :]) > 0
        # poly_mask = cone_of_vision_mask
        # poly_mask = distance_mask
        # poly_mask = front_facing_mask
        poly_mask = distance_mask & cone_of_vision_mask & front_facing_mask
        eligible_polys = np.where(poly_mask)[0]
        depth_coords = [(distance[i], i) for i in eligible_polys]
        depth_coords.sort(reverse=True)

        def light_components():

            for light in scene.lights:

                if isinstance(light, DirectionalLight):
                    light_dot_products = np.dot(light.direction, normals[:3, :])
                    intensities = np.clip(light_dot_products, 0, 1)

                elif isinstance(light, PointLight):
                    point_light_vector = centers[:3, :] - np.expand_dims(light.position.A, 1)
                    d = np.linalg.norm(point_light_vector, axis=0)
                    point_light_normals = point_light_vector / d
                    # https://stackoverflow.com/questions/14758283/is-there-a-numpy-scipy-dot-product-calculating-only-the-diagonal-entries-of-the
                    point_light_dot_products = (point_light_normals * normals[:3, :]).sum(axis=0)
                    intensities = np.clip(point_light_dot_products, 0, 1)

                elif isinstance(light, AmbientLight):
                    repeats = len(polys)
                    intensities = np.repeat(light.intensity, repeats)

                yield intensities

        lighting = np.vstack(tuple(light_components())).sum(axis=0)

        for z, i in depth_coords:
            l = lighting[i]
            p1, p2, p3 = polys[i]
            x1, y1 = points[0, p1], points[1, p1]
            x2, y2 = points[0, p2], points[1, p2]
            x3, y3 = points[0, p3], points[1, p3]
            lit_color = tuple(map(lambda x: np.clip(l * x, 0, 1), colors[i]))
            self.draw_poly(x1, y1, x2, y2, x3, y3, lit_color)

    def render(self, scene):

        self.prerender()
        if self._clear:
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
            vertices.append(obj.transformed_vertices)
            normals.append(obj.transformed_normals)
            centers.append(obj.transformed_centers)
            if obj.edges:
                obj_edges = [((edge[0]+n_points), (edge[1] + n_points)) for edge in obj.edges]
                edges.append(obj_edges)

            obj_polys = [((poly[0]+n_points), (poly[1] + n_points), (poly[2] + n_points)) for poly in obj.polys]
            colors.extend([obj.color.as_tuple() for _ in obj.polys])
            polys.extend(obj_polys)

            n_points += obj.vertices.shape[1]

        vertices_matrix = np.hstack(vertices)
        normals_matrix = np.hstack(normals)
        centers_matrix = np.hstack(centers)

        points = self.vertices_to_screen(scene, vertices_matrix)

        if edges and self._draw_edges:
            self.draw_edges(points, edges, colors)
        if self._draw_polys:
            self.draw_polys(scene, normals_matrix, centers_matrix, points, polys, colors)
        if self._draw_wireframe:
            self.draw_wireframe(points, polys, colors)

        if self._draw_centers:
            center_points = self.vertices_to_screen(scene, centers_matrix)
            self.draw_centers(center_points)
        if self._draw_axes:
            self.draw_axes(scene)

        self.postrender()

    def vertices_to_screen(self, scene, vertices):
        transformed_vertices = np.linalg.inv(scene.main_camera.R) @ np.linalg.inv(scene.main_camera.T) @ vertices
        # perspective
        transformed_vertices[:3, :] /= transformed_vertices[2, :]

        camera_points = scene.main_camera.matrix() @ transformed_vertices
        camera_points2d = camera_points[:2, :]
        scale = min(self.width, self.height) * self.pixel_aspect
        xscale = scale * self.pixel_aspect
        yscale = scale * (1/self.pixel_aspect)
        camera_points2d[0, :] = camera_points2d[0, :]*xscale + (self.width-xscale)/2
        camera_points2d[1, :] = camera_points2d[1, :]*yscale + (self.height-yscale)/2
        points_int = camera_points2d.astype(np.int32)
        return points_int
