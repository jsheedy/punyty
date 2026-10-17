class DirectionalLight():
    def __init__(self, direction):
        self.direction = direction.normalize().A


class PointLight():
    def __init__(self, position, intensity=1.0):
        self.position = position
        self.intensity = intensity


class AmbientLight():
    def __init__(self, intensity=0.1):
        self.intensity = intensity

