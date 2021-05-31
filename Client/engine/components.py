from utils import Vec2d
from time import time_ns as get_time


class RenderComponent:
    def __init__(self, img_name=None, size=None, fixed_orient=False, fixed_size=False):
        self.img_name = img_name
        self.fixed_size = fixed_size
        self.fixed_orient = fixed_orient
        self.size = size


class PositionComponent:
    def __init__(self, pos=Vec2d(0, 0), orient=Vec2d(1, 0), z=0):
        self.orient = orient
        self.pos = pos
        self.z = z


class ShootingComponent:
    def __init__(self, reload_time=0.5, bullet_speed=700, reload_mine_time=1):
        self.reload_time = reload_time  # in seconds
        self.reload_mine_time = reload_mine_time
        self.bullet_speed = bullet_speed  # initial bullet speed
        self.last_time_shot = 0
        self.last_time_mine = 0


class ControlComponent:
    def __init__(self, player=None):
        self.player = player
        self.rotation_speed = 2.4
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
    def __init__(self, curr_hp=1000, max_hp=1000):
        self.curr_hp = curr_hp
        self.max_hp = max_hp
        self.last_time_hit = 0


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


class AnimationComponent:
    def __init__(self, img_num=1, img_name='explosion'):
        self.img_name = img_name
        self.img_num = img_num
        self.curr_img_idx = -1
        self.entire_time = 0.4 * 1e9
        self.change_time = self.entire_time / self.img_num
        self.last_time_changed = 0


class HitComponent:
    def __init__(self, dmg=100, owner_id=None, activ_time=0):
        self.time_placed = get_time()
        self.activation_time = activ_time
        self.dmg = dmg
        self.owner_id = owner_id


