from utils import Vec2d


class RenderComponent:
    def __init__(self, img='', size=(10, 10)):
        self.img = img
        self.size = size


class PositionComponent:
    def __init__(self, pos=Vec2d(0, 0), orient=Vec2d(1, 0), z=0):
        self.orient = orient
        self.pos = pos
        self.z = z


class ShootingComponent:
    def __init__(self, reload_time=1.5, bullet_speed=1000):
        self.reload_time = reload_time  # in seconds
        self.bullet_speed = bullet_speed  # initial bullet speed
        self.last_time_shot = 0


class ControlComponent:
    def __init__(self, player=None):
        self.player = player
        self.rotation_speed = 1.8
        self.engine_acc_forward = 20000
        self.engine_acc_backward = 5000


class DynamicsComponent:
    def __init__(self, vel=Vec2d(0, 0), force=Vec2d(0, 0), mass=None):
        self.vel = vel
        self.force = force
        self.inverse_mass = 0
        if mass:
            self.inverse_mass = 1 / mass


class HealthComponent:
    def __init__(self, cur_hp=0, max_hp=100):
        self.cur_hp = cur_hp
        self.max_hp = max_hp
        self.alive = True


class HitboxComponent:
    def __init__(self, size=(0, 0)):
        self.name = __name__.split('.')[-1]
        self.vertices = [Vec2d(size[0] / (-2), size[1] / (-2)),  # bottom left
                         Vec2d(size[0] / 2, size[1] / (-2)),  # bottom right
                         Vec2d(size[0] / 2, size[1] / 2),  # top right
                         Vec2d(size[0] / (-2), size[1] / 2)]  # top left
        self.transformed_vertices = [None] * len(self.vertices)
        self.overlap = False
        self.is_dirty = True
        self.r_squared = (size[0] / 2) ** 2 + (size[1] / 2) ** 2



