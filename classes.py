import math


class Dot:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Dot(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Dot(self.x - other.x, self.y - other.y, self.z - other.z)


class Vector:
    def __init__(self, dot):
        self.coord = dot
        self.x = dot.x
        self.y = dot.y
        self.z = dot.z

    def length(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

    def __add__(self, other):
        return Vector(self.coord + other)

    def __sub__(self, other):
        return Vector(self.coord - other)

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __truediv__(self, other):
        return Vector(Dot(self.coord.x / other, self.coord.y / other, self.coord.z / other))


class Line(Vector):
    def __init__(self, dot, start_dot):
        super().__init__(dot)
        self.x_0 = start_dot.x
        self.y_0 = start_dot.y
        self.z_0 = start_dot.z


class Ray(Line):
    def __init__(self, dot, start_dot, color):
        super().__init__(dot, start_dot)
        self.color = color


class Surface:
    def __init__(self, dot1, dot2, dot3, color, name=None, k_a=0.2, k_d=1, k_s=10, p=6, transparency=0, n=1,
                 reflection=0):
        self.color = color
        self.name = name
        v12 = Vector(dot2 - dot1)
        v13 = Vector(dot3 - dot1)
        # from determinant of matrix |i   j   k  |
        # calculate normal vector    |x_0 y_0 z_0|
        # and all surface            |x_1 y_1 z_1|
        a = v12.y * v13.z - v12.z * v13.y
        b = v12.z * v13.x - v12.x * v13.z
        c = v12.x * v13.y - v12.y * v13.x
        self.normal_vec = Vector(Dot(a, b, c))
        # from normal vector and equation n_x * (x - x_0) + n_y * (y - y_0) + n_z * (z - z_0) = 0
        # calculate ax + by + cz + d = 0
        self.a = a
        self.b = b
        self.c = c
        self.d = -a * dot1.x - b * dot1.y - c * dot1.z
        self.k_a = k_a
        self.k_d = k_d
        self.k_s = k_s
        self.p = p
        self.trans = transparency
        self.n = n
        self.reflection = reflection

    def is_intersect(self, ray):
        if ray * self.normal_vec == 0:
            return False
        # from parametric equation of ray and equation of surface receive:
        p_1 = ray.x
        p_2 = ray.y
        p_3 = ray.z
        t = (-(self.a * ray.x_0 + self.b * ray.y_0 + self.c * ray.z_0 + self.d)) / \
            (self.a * p_1 + self.b * p_2 + self.c * p_3)
        if t <= 0:
            return False
        return [Dot(t * ray.x + ray.x_0, t * ray.y + ray.y_0, t * ray.z + ray.z_0)]

    def normal(self, dot):
        return self.normal_vec


class Sphere:
    def __init__(self, center, radius, color, name=None, k_a=0.2, k_d=1, k_s=20, p=5, transparency=0, n=1,
                 reflection=0.3):
        self.center = center
        self.r = radius
        self.color = color
        self.name = name
        self.k_a = k_a
        self.k_d = k_d
        self.k_s = k_s
        self.p = p
        self.trans = transparency
        self.n = n
        self.reflection = reflection

    def is_intersect(self, ray):
        p_1 = ray.x
        p_2 = ray.y
        p_3 = ray.z
        x_0 = ray.x_0
        y_0 = ray.y_0
        z_0 = ray.z_0
        a = self.center.x
        b = self.center.y
        c = self.center.z
        # from equation of sphere and parametric equation of ray, after some algebraic calculation, receive equation:
        # (p_1 ** 2 + p_2 ** 2 + p_3 ** 2) * t**2 + 2 * (p_1 * (x_0 - a) + p_2 * (y_0 - b) + p_3 * (z_0 - c)) * t +
        # + (x_0 - a) ** 2 + (y_0 - b) ** 2 + (z_0 - c) ** 2 - r ** 2 = 0
        # go to at**2 + bt + c = 0
        a_t = (p_1 ** 2 + p_2 ** 2 + p_3 ** 2)
        b_t = 2 * (p_1 * (x_0 - a) + p_2 * (y_0 - b) + p_3 * (z_0 - c))
        c_t = (x_0 - a) ** 2 + (y_0 - b) ** 2 + (z_0 - c) ** 2 - self.r ** 2
        discriminant = b_t ** 2 - 4 * a_t * c_t
        if discriminant < 0:
            return False
        elif discriminant == 0:
            t = -b_t / (2 * a_t)
            if t <= 0:
                return False
            return [Dot(p_1 * t + x_0, p_2 * t + y_0, p_3 * t + z_0)]
        t_1 = (-b_t + discriminant ** 0.5) / (2 * a_t)
        t_2 = (-b_t - discriminant ** 0.5) / (2 * a_t)
        dots = []
        for t in [t_1, t_2]:
            if t <= 0:
                continue
            # TODO: need to add epsilon to avoid artefacts. Need to add epsilon in way of ray
            dots.append(Dot(p_1 * t + x_0, p_2 * t + y_0, p_3 * t + z_0))
        return dots

    def find_tangent_in_dot(self, dot):
        # from M_0(x_0, y_0, z_0) and F(x, y, z) calculate tangent surface which is
        # F_x'(M_0) * (x - x_0) + F_y'(M_0) * (y - y_0) + F_z'(M_0) * (z - z_0) = 0
        # after some algebraic calculations receive
        x_0 = dot.x
        y_0 = dot.y
        z_0 = dot.z
        a = self.center.x
        b = self.center.y
        c = self.center.z
        # make new Surface from 3 dots
        try:
            dot2 = Dot(0, 0, (x_0 ** 2 + y_0 ** 2 + z_0 ** 2 - a * x_0 - b * y_0 - c * z_0) / (z_0 - c))
            dot3 = Dot((x_0 ** 2 + y_0 ** 2 + z_0 ** 2 - a * x_0 - b * y_0 - c * z_0) / (x_0 - a), 0, 0)
            return Surface(dot, dot2, dot3, [0, 0, 0])
        except:
            return Surface(dot, Dot(0, 0, 1), Dot(1, 1, 0), [0, 0, 0])

    def normal(self, dot):
        surface = self.find_tangent_in_dot(dot)
        return surface.normal(dot)
