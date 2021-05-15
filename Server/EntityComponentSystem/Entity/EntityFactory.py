from random import randint, random

import pygame
from pygame.locals import *

from EntityComponentSystem.Components.ButtonComponent import ButtonComponent
from EntityComponentSystem.Components.DynamicsComponent import DynamicsComponent
from EntityComponentSystem.Components.HitboxComponent import HitboxComponent
from EntityComponentSystem.Components.PositionComponent import PositionComponent
from EntityComponentSystem.Components.RenderComponent import RenderComponent
from EntityComponentSystem.Components.ControlComponent import ControlComponent
from EntityComponentSystem.Components.ShootingComponent import ShootingComponent
from EntityComponentSystem.Components.TextFieldComponent import TextFieldComponent
from utils.Vec2d import Vec2d
from Main.settings import SCR_HEIGHT
from Main.settings import SCR_WIDTH


class EntityFactory:

    def __init__(self, entity_manager):
        self._entity_manager = entity_manager

    def create_tank1(self):
        pos = Vec2d(SCR_WIDTH / 2, SCR_HEIGHT / 2)
        size = 150, 70
        entity = self._entity_manager.create_entity("czolg")
        self._entity_manager.add_component(DynamicsComponent(mass=10), entity)
        self._entity_manager.add_component(PositionComponent(pos=pos), entity)
        self._entity_manager.add_component(RenderComponent('test_tank.png', size), entity)
        self._entity_manager.add_component(ShootingComponent(), entity)
        self._entity_manager.add_component(HitboxComponent(size), entity)
        return entity

    def create_protagonist(self):
        entity = self.create_tank1()
        self._entity_manager.add_component(ControlComponent('player one'), entity)

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

    def create_obstacles(self):
        TILE_SIZE = 60, 60

        for i in range(3):
            entity = self._entity_manager.create_entity("przeszkoda {}".format(i))
            x = randint(100, 1000)
            y = randint(100, 600)
            self._entity_manager.add_component(PositionComponent(pos=Vec2d(x, y)), entity)
            self._entity_manager.add_component(DynamicsComponent(), entity)
            self._entity_manager.add_component(RenderComponent('brown_square.png', TILE_SIZE), entity)
            self._entity_manager.add_component(HitboxComponent(TILE_SIZE), entity)

    def create_menu_background(self):
        e = self._entity_manager.create_entity("tlo")
        self._entity_manager.add_component(RenderComponent('log_back.jpg', (SCR_WIDTH, SCR_HEIGHT)), e)
        self._entity_manager.add_component(PositionComponent(Vec2d(SCR_WIDTH / 2, SCR_HEIGHT / 2), z=10), e)

    def create_text_field(self, to_cen, active):
        e = self._entity_manager.create_entity("text input")
        self._entity_manager.add_component(RenderComponent('input_back.jpg', (300, 30)), e)
        self._entity_manager.add_component(PositionComponent(Vec2d(SCR_WIDTH/2, SCR_HEIGHT/2+to_cen), z=10), e)
        self._entity_manager.add_component(TextFieldComponent(active=active), e)

    def create_button(self, to_cen, tex, login):
        e = self._entity_manager.create_entity("button")
        self._entity_manager.add_component(RenderComponent(tex, (200, 30)), e)
        self._entity_manager.add_component(ButtonComponent(login), e)
        self._entity_manager.add_component(PositionComponent(Vec2d(SCR_WIDTH / 2, SCR_HEIGHT / 2 + to_cen), z=10), e)

