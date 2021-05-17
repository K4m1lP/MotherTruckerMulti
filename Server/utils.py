from math import sqrt, sin, cos, atan2, pi

class Vec2d:
    def __init__(self, x=0., y=0.):
        self.x = x
        self.y = y

    def add(self, other):
        return Vec2d(self.x + other.x, self.y + other.y)

    def scale(self, scalar):
        return Vec2d(self.x * scalar, self.y * scalar)

    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def gt(self, other):
        return self.length() > other.length()

    def normalize(self):
        if self.length() > 0:
            length = self.length()
            self.x *= 1 / length
            self.y *= 1 / length

    def rotate(self, alpha):
        new_orient_x = cos(alpha) * self.x - sin(alpha) * self.y
        new_orient_y = sin(alpha) * self.x + cos(alpha) * self.y
        return Vec2d(new_orient_x, new_orient_y)

    def get_angle(self):
        self.normalize()
        return (atan2(self.y, self.x) / (2 * pi) * 360) % 360 * (-1)

    def __repr__(self):
        return str(self.x) + ", " + str(self.y)

    def get_perp(self):  # get vector perpendicular to the given
        return Vec2d(-self.y, self.x)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def get_angle_normalnie(self):
        return atan2(self.y, self.x)


class Player:
    __next_free_idx = 0

    def __init__(self, nick):
        self.nick = nick
        self.keys = None
        self.id = Player.__next_free_idx
        Player.__next_free_idx += 1


class GameState:
    def __init__(self):
        self.to_render = []
        self.has_ended = False
        self.winner = None
        self.frame_time = None


class Sprite:
    def __init__(self, pos_comp, render_comp):
        self.pos = pos_comp.pos
        self.z = pos_comp.z
        self.img_name = render_comp.img_name
        self.size = render_comp.size
        self.orient = pos_comp.orient
        self.fixed_size = render_comp.fixed_size
        self.fixed_orient = render_comp.fixed_orient
