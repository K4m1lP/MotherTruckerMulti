from engine.components import *
from settings import *


class EntityManager:
    def __init__(self):
        self._entities = []
        self._components = {}
        self._lowest_id = 0
        self.max_int = 10000
        self.entity_counter = 0
        self.entity_names = {}

    def remove_entity(self, entity_int):
        for comp_name in self._components.keys():
            if entity_int in self._components[comp_name].keys():
                self._components[comp_name].pop(entity_int)
        self.entity_counter -= 1
        self.entity_names.pop(entity_int)
        self._entities.remove(entity_int)

    def entity_number(self):
        return self.entity_counter

    def _new_id(self):
        if self._lowest_id < self.max_int:
            self._lowest_id += 1
            return self._lowest_id
        else:
            try:
                for i in range(1, self.max_int):
                    if not self._entities.__contains__(i):
                        return i
            except ValueError:
                print("Brakło inta czy coś, do zbadania")

    def create_entity(self, name):
        new_id = self._new_id()
        self._entities.append(new_id)
        self.entity_names[new_id] = name
        self.entity_counter += 1
        return new_id

    def add_component(self, comp, entity_int):
        if comp.__class__.__name__ not in self._components.keys():
            self._components[comp.__class__.__name__] = {}
        self._components[comp.__class__.__name__][entity_int] = comp

    def get_component_of_class(self, comp, entity):
        if comp.__class__.__name__ in self._components and entity in self._components[comp.__class__.__name__]:
            return self._components[comp.__class__.__name__][entity]

    def get_all_entities_possessing_component_of_class(self, comp):
        if comp.__class__.__name__ not in self._components:
            return []
        else:
            return list(self._components[comp.__class__.__name__].keys())


class EntityFactory:

    def __init__(self, entity_manager):
        self._entity_manager = entity_manager

    def create_tank(self, texture_id, pos):
        if not (texture_id == 0 or texture_id == 1):
            print("Error: Entity factory: create_tank: Wrong texture id, can be 0 or 1")
            exit(1)
        size = 150, 70
        entity = self._entity_manager.create_entity("czolg")
        self._entity_manager.add_component(DynamicsComponent(mass=10), entity)
        self._entity_manager.add_component(PositionComponent(pos=Vec2d(pos[0], pos[1]), z=1), entity)
        self._entity_manager.add_component(RenderComponent('tank{}.png'.format(texture_id), size), entity)
        self._entity_manager.add_component(ShootingComponent(), entity)
        self._entity_manager.add_component(HitboxComponent(size), entity)
        self._entity_manager.add_component(HealthComponent(1000, 1000), entity)
        return entity

    def create_protagonist(self, player, pos):
        entity = self.create_tank(player.id, pos)
        self._entity_manager.add_component(ControlComponent(player), entity)

    def create_background(self):
        pos = Vec2d(SCR_WIDTH / 2, SCR_HEIGHT / 2)
        entity = self._entity_manager.create_entity("tło")
        self._entity_manager.add_component(PositionComponent(pos=pos, z=0), entity)
        self._entity_manager.add_component(RenderComponent('background.png', None, True, True), entity)

    def create_bullet(self, pos, orient, speed, owner_id):
        entity = self._entity_manager.create_entity("pocisk")
        self._entity_manager.add_component(PositionComponent(pos=pos, orient=orient, z=2), entity)
        self._entity_manager.add_component(DynamicsComponent(vel=orient.scale(speed), mass=1), entity)
        self._entity_manager.add_component(RenderComponent('bullet.png', None, False, True), entity)
        self._entity_manager.add_component(HitComponent(250, owner_id), entity)
        self._entity_manager.add_component(HitboxComponent((30, 17)), entity)

    def create_border_walls(self):
        WALL_THICKNESS = 30
        # ---------------------- LEWA SCIANA --------------
        vert_wall_size = WALL_THICKNESS, SCR_HEIGHT
        entity = self._entity_manager.create_entity("sciana lewa")
        self._entity_manager.add_component(PositionComponent(pos=Vec2d(WALL_THICKNESS / 2, SCR_HEIGHT / 2), z=1),
                                           entity)
        self._entity_manager.add_component(DynamicsComponent(), entity)
        self._entity_manager.add_component(RenderComponent('vert_wall.png', vert_wall_size, True, True), entity)
        self._entity_manager.add_component(HitboxComponent(vert_wall_size), entity)

        # ---------------------- PRAWA SCIANA --------------
        entity = self._entity_manager.create_entity("sciana prawa")
        self._entity_manager.add_component(
            PositionComponent(pos=Vec2d(SCR_WIDTH - (WALL_THICKNESS / 2), SCR_HEIGHT / 2), z=1), entity)
        self._entity_manager.add_component(DynamicsComponent(), entity)
        self._entity_manager.add_component(RenderComponent('vert_wall.png', vert_wall_size, True, True), entity)
        self._entity_manager.add_component(HitboxComponent(vert_wall_size), entity)

        # ---------------------- GORNA SCIANA --------------
        horiz_wall_size = SCR_WIDTH, WALL_THICKNESS
        entity = self._entity_manager.create_entity("sciana gorna")
        self._entity_manager.add_component(PositionComponent(pos=Vec2d(SCR_WIDTH / 2, WALL_THICKNESS / 2), z=1), entity)
        self._entity_manager.add_component(DynamicsComponent(), entity)
        self._entity_manager.add_component(RenderComponent('horiz_wall.png', horiz_wall_size, True, True), entity)
        self._entity_manager.add_component(HitboxComponent(horiz_wall_size), entity)

        # ---------------------- DOLNA SCIANA --------------
        entity = self._entity_manager.create_entity("sciana dolna")
        self._entity_manager.add_component(
            PositionComponent(pos=Vec2d(SCR_WIDTH / 2, SCR_HEIGHT - (WALL_THICKNESS / 2)), z=1), entity)
        self._entity_manager.add_component(DynamicsComponent(), entity)
        self._entity_manager.add_component(RenderComponent('horiz_wall.png', horiz_wall_size, True, True), entity)
        self._entity_manager.add_component(HitboxComponent(horiz_wall_size), entity)

    def create_explosion(self, pos, size=(DEFAULT_EXPLOSION_SIZE, DEFAULT_EXPLOSION_SIZE)):
        entity = self._entity_manager.create_entity("eksplozja")
        self._entity_manager.add_component(PositionComponent(pos=pos, z=2), entity)
        self._entity_manager.add_component(RenderComponent('explosion0.png', size, True, True), entity)
        self._entity_manager.add_component(AnimationComponent(img_num=6, img_name='explosion'), entity)

    def create_mine(self, pos, owner_id):
        entity = self._entity_manager.create_entity("mina")
        self._entity_manager.add_component(PositionComponent(pos=pos, z=1), entity)
        self._entity_manager.add_component(RenderComponent('mine.png', None, True, True), entity)
        self._entity_manager.add_component(HitComponent(500, owner_id, activ_time=(2 * 1e9)), entity)
        self._entity_manager.add_component(HitboxComponent((28, 28)), entity)
        self._entity_manager.add_component(DynamicsComponent(), entity)


class Collision:
    def __init__(self, ent1, ent2, pen_length, pen_vec):
        self.pen_length = pen_length
        self.pen_vec = pen_vec
        self.ent1 = ent1
        self.ent2 = ent2


class CollisionManager:
    __instance = None

    @staticmethod
    def get_instance():
        if not CollisionManager.__instance:
            CollisionManager()
        return CollisionManager.__instance

    def __init__(self):
        if CollisionManager.__instance:
            raise Exception("Class is a singleton!")
        else:
            CollisionManager.__instance = self

            self._collisions_q = []

    def add_collision(self, col):
        self._collisions_q.append(col)

    def get_collisions(self):
        res = self._collisions_q
        self._collisions_q = []
        return res
