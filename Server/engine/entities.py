from engine.components import *
from settings import *


class Entity:
    def __init__(self, my_id, entity_manager):
        self.my_id = my_id
        self.entity_manager = entity_manager


class EntityManager:
    """
    Klasa której zadaaniem jest przechowywanie informacji o obecnie istniejących entity
    wraz z ich komponentami, jest niczym baza danych a zastosowana struktura
    wygląda następująco:
    {
        "ComponentName": { (int)Entity.id : ComponentObject }
    }
    przykład:
    {
        "HealthComponent": { 1 : (Object)<adres w pamięci> },
        "MoveComponent": { 1 : (Object)<adres w pamięci>, 2 : (Object)<adres w pamięci> }
    }
    """
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

    def get_entities_with_comp(self, comp):
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
        self._entity_manager.add_component(PositionComponent(pos=Vec2d(pos[0], pos[1])), entity)
        self._entity_manager.add_component(RenderComponent('tank{}.png'.format(texture_id), size), entity)
        self._entity_manager.add_component(ShootingComponent(), entity)
        self._entity_manager.add_component(HitboxComponent(size), entity)
        return entity

    def create_protagonist(self, player, pos):
        entity = self.create_tank(player.id, pos)
        self._entity_manager.add_component(ControlComponent(player), entity)

    def create_background(self):
        pos = Vec2d(SCR_WIDTH / 2, SCR_HEIGHT / 2)
        size = SCR_WIDTH, SCR_HEIGHT
        entity = self._entity_manager.create_entity("tło")
        self._entity_manager.add_component(PositionComponent(pos=pos), entity)
        self._entity_manager.add_component(RenderComponent('background.png', size), entity)

    def create_bullet(self, pos, orient, speed):
        size = 37, 13
        entity = self._entity_manager.create_entity("pocisk")
        self._entity_manager.add_component(PositionComponent(pos=pos, orient=orient, z=1), entity)
        self._entity_manager.add_component(DynamicsComponent(vel=orient.scale(speed), mass=1), entity)
        self._entity_manager.add_component(RenderComponent('bullet.png', size), entity)
        self._entity_manager.add_component(HitboxComponent(size), entity)

    def create_border_walls(self):
        WALL_THICKNESS = 30
        # ---------------------- LEWA SCIANA --------------
        vert_wall_size = WALL_THICKNESS, SCR_HEIGHT
        entity = self._entity_manager.create_entity("sciana lewa")
        self._entity_manager.add_component(PositionComponent(pos=Vec2d(WALL_THICKNESS / 2, SCR_HEIGHT / 2)), entity)
        self._entity_manager.add_component(DynamicsComponent(), entity)
        self._entity_manager.add_component(RenderComponent('vert_wall.png', vert_wall_size), entity)
        self._entity_manager.add_component(HitboxComponent(vert_wall_size), entity)

        # ---------------------- PRAWA SCIANA --------------
        entity = self._entity_manager.create_entity("sciana prawa")
        self._entity_manager.add_component(
            PositionComponent(pos=Vec2d(SCR_WIDTH - (WALL_THICKNESS / 2), SCR_HEIGHT / 2)), entity)
        self._entity_manager.add_component(DynamicsComponent(), entity)
        self._entity_manager.add_component(RenderComponent('vert_wall.png', vert_wall_size), entity)
        self._entity_manager.add_component(HitboxComponent(vert_wall_size), entity)

        # ---------------------- GORNA SCIANA --------------
        horiz_wall_size = SCR_WIDTH, WALL_THICKNESS
        entity = self._entity_manager.create_entity("sciana gorna")
        self._entity_manager.add_component(PositionComponent(pos=Vec2d(SCR_WIDTH / 2, WALL_THICKNESS / 2)), entity)
        self._entity_manager.add_component(DynamicsComponent(), entity)
        self._entity_manager.add_component(RenderComponent('horiz_wall.png', horiz_wall_size), entity)
        self._entity_manager.add_component(HitboxComponent(horiz_wall_size), entity)

        # ---------------------- DOLNA SCIANA --------------
        entity = self._entity_manager.create_entity("sciana dolna")
        self._entity_manager.add_component(
            PositionComponent(pos=Vec2d(SCR_WIDTH / 2, SCR_HEIGHT - (WALL_THICKNESS / 2))), entity)
        self._entity_manager.add_component(DynamicsComponent(), entity)
        self._entity_manager.add_component(RenderComponent('horiz_wall.png', horiz_wall_size), entity)
        self._entity_manager.add_component(HitboxComponent(horiz_wall_size), entity)
