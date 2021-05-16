import pygame
import random
from time import time_ns as get_time
import math

from EntityComponentSystem.System.System import System
from EntityComponentSystem.Components.DynamicsComponent import DynamicsComponent
from EntityComponentSystem.Components.PositionComponent import PositionComponent
from EntityComponentSystem.Components.ShootingComponent import ShootingComponent


class ShootingSystem(System):
    def __init__(self, entity_manager, entity_factory):
        super().__init__(entity_manager)
        self.entity_factory = entity_factory
        self.key_listener = None

    def update(self, dt):
        entities = self.entity_manager.get_all_entities_possessing_component_of_class(ShootingComponent())

        for entity in entities:
            shooting_comp = self.entity_manager.get_component_of_class(ShootingComponent(), entity)
            pos_comp = self.entity_manager.get_component_of_class(PositionComponent(), entity)
            dynamics_comp = self.entity_manager.get_component_of_class(DynamicsComponent(), entity)

            if pos_comp and dynamics_comp:
                if self.key_listener.is_pressed(pygame.K_SPACE):
                    time_since_last_shot = (get_time() * 1e-9) - shooting_comp.last_time_shot
                    if time_since_last_shot > shooting_comp.reload_time:
                        # inaccuracy mechanism
                        shot_angle = 0
                        if dynamics_comp.vel.length() > 0:
                            max_angle = 2 / (math.pi * 2)
                            shot_angle = (random.random() * max_angle) - (max_angle / 2)
                        bullet_orient = pos_comp.orient.rotate(shot_angle)
                        self.entity_factory.create_bullet(pos_comp.pos.add(pos_comp.orient.scale(95)), bullet_orient,
                                                          shooting_comp.bullet_speed)
                        shooting_comp.last_time_shot = get_time() * 1e-9
