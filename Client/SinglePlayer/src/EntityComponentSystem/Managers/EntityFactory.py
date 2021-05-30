import os
from random import randint

from SinglePlayer.src.EntityComponentSystem.Components.AnimationComponent import AnimationComponent
from SinglePlayer.src.EntityComponentSystem.Components.ControlComponent import ControlComponent
from SinglePlayer.src.EntityComponentSystem.Components.DynamicsComponent import DynamicsComponent
from SinglePlayer.src.EntityComponentSystem.Components.HealthComponent import HealthComponent
from SinglePlayer.src.EntityComponentSystem.Components.HitComponent import HitComponent
from SinglePlayer.src.EntityComponentSystem.Components.HitboxComponent import HitboxComponent
from SinglePlayer.src.EntityComponentSystem.Components.PositionComponent import PositionComponent
from SinglePlayer.src.EntityComponentSystem.Components.RenderComponent import RenderComponent
from SinglePlayer.src.EntityComponentSystem.Components.ShootingComponent import ShootingComponent
from SinglePlayer.src.settings import SCR_HEIGHT, DEFAULT_EXPLOSION_SIZE
from SinglePlayer.src.utils.Vec2d import Vec2d
from settings import SCR_WIDTH


class EntityFactory:

    def __init__(self, entity_manager):
        self._entity_manager = entity_manager

    def create_tank1(self, id, pos):
        if id == 0: orient = Vec2d(-1, 0)
        else: orient = Vec2d(1, 0)
        size = 150, 70
        entity = self._entity_manager.create_entity("czolg")
        self._entity_manager.add_component(DynamicsComponent(mass=10), entity)
        self._entity_manager.add_component(PositionComponent(pos=Vec2d(pos[0], pos[1]), orient=orient, z=1), entity)
        if id == 0:
            self._entity_manager.add_component(RenderComponent('dark_tank0.png'.format(id), size), entity)
            self._entity_manager.add_component(AnimationComponent(2, 'dark_tank'), entity)
        else:
            self._entity_manager.add_component(RenderComponent('light_tank0.png'.format(id), size), entity)
            self._entity_manager.add_component(AnimationComponent(2, 'light_tank'), entity)
        self._entity_manager.add_component(ShootingComponent(), entity)
        self._entity_manager.add_component(HitboxComponent(size), entity)
        self._entity_manager.add_component(HealthComponent(1000, 1000), entity)
        return entity

    def create_player(self, id, pos):
        if not (id == 0 or id == 1):
            print("Wrong id in entity factory, program exit")
            exit(0)
        entity = self.create_tank1(id, pos)
        self._entity_manager.add_component(ControlComponent(id, 'player one'), entity)

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
        WALL_THICKNESS = 50
        # ---------------------- LEWA SCIANA --------------
        vert_wall_size = WALL_THICKNESS, SCR_HEIGHT
        entity = self._entity_manager.create_entity("sciana lewa")
        self._entity_manager.add_component(PositionComponent(pos=Vec2d(WALL_THICKNESS / 2, SCR_HEIGHT / 2), z=1), entity)
        self._entity_manager.add_component(DynamicsComponent(), entity)
        self._entity_manager.add_component(RenderComponent('vert_wall.png', None, True, True), entity)
        self._entity_manager.add_component(HitboxComponent(vert_wall_size), entity)

        # ---------------------- PRAWA SCIANA --------------
        entity = self._entity_manager.create_entity("sciana prawa")
        self._entity_manager.add_component(
            PositionComponent(pos=Vec2d(SCR_WIDTH - (WALL_THICKNESS / 2), SCR_HEIGHT / 2), z=1), entity)
        self._entity_manager.add_component(DynamicsComponent(), entity)
        self._entity_manager.add_component(RenderComponent('vert_wall.png', None, True, True), entity)
        self._entity_manager.add_component(HitboxComponent(vert_wall_size), entity)

        # ---------------------- GORNA SCIANA --------------
        horiz_wall_size = SCR_WIDTH, WALL_THICKNESS
        entity = self._entity_manager.create_entity("sciana gorna")
        self._entity_manager.add_component(PositionComponent(pos=Vec2d(SCR_WIDTH / 2, WALL_THICKNESS / 2), z=1), entity)
        self._entity_manager.add_component(DynamicsComponent(), entity)
        self._entity_manager.add_component(RenderComponent('horiz_wall.png', None, True, True), entity)
        self._entity_manager.add_component(HitboxComponent(horiz_wall_size), entity)

        # ---------------------- DOLNA SCIANA --------------
        entity = self._entity_manager.create_entity("sciana dolna")
        self._entity_manager.add_component(
            PositionComponent(pos=Vec2d(SCR_WIDTH / 2, SCR_HEIGHT - (WALL_THICKNESS / 2)), z=1), entity)
        self._entity_manager.add_component(DynamicsComponent(), entity)
        self._entity_manager.add_component(RenderComponent('horiz_wall.png', None, True, True), entity)
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

    def create_tile(self, pos, tile_size):
        entity = self._entity_manager.create_entity("tile")
        self._entity_manager.add_component(PositionComponent(pos=pos, z=1), entity)
        self._entity_manager.add_component(DynamicsComponent(), entity)
        self._entity_manager.add_component(RenderComponent('tile.png', (tile_size, tile_size), True, True), entity)
        self._entity_manager.add_component(HitboxComponent((tile_size, tile_size)), entity)

    def create_obstacles_from_file(self, filename):
        delimiter = ', '
        file = open(os.path.join('assets/maps/', filename), "r")
        # read headers (three lines)
        tile_size = int(file.readline())
        tiles_width = int(file.readline())
        tiles_height = int(file.readline())
        # read proper tile template
        for i in range(tiles_height):
            tiles_row_str = file.readline()
            tiles_row = [int(x) for x in tiles_row_str.split(delimiter) if x.strip()]
            for j in range(tiles_width):
                if tiles_row[j] == 1:
                    self.create_tile(Vec2d(tile_size / 2 + tile_size * (j+1), tile_size / 2 + tile_size * (i+1)), tile_size)
        file.close()
