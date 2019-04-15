import math


class ZeroVectorError(Exception): pass


class Vector3:

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def unity(cls):
        return cls(1,1,1)

    def __add__(self, other):
        return Vector3(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __sub__(self, other):
        return self + -other

    def __mul__(self, s):
        return Vector3(self.x * s, self.y * s, self.z * s)

    def __rmul__(self, s):
        return self * s

    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)

    def __repr__(self):
        return "Vector3([{} {} {}])".format(self.x, self.y, self.z)

    @classmethod
    def zero(cls):
        """returns Vector(0,0,0)"""
        return cls(0, 0, 0)

    def length(self):
        """ returns the magnitude of this vector """
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        """ cross product for left handed coordinate system """
        a = self
        b = other
        return -1 * Vector3(
            a.y * b.z - a.z * b.y,
            a.z * b.x - a.x * b.z,
            a.x * b.y - a.y * b.x
        )

    def angle_between(self, other):
        """ returns the angle between this vector and other """
        dot = self.normalize().dot(other.normalize())
        angle = math.acos(dot)  # / (self.length() * other.length()))
        return angle

    def normalize(self):
        """ returns a vector in the same direction with unit length
        In the degenerate case of a zero vector, raises"""

        length = self.length()
        if length == 0:
            raise ZeroVectorError("can't normalize 0 vector")
        return Vector3(self.x / length, self.y / length, self.z / length)
