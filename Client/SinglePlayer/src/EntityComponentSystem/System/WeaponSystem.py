import os

import pygame
import random
from time import time_ns as get_time
import math

from SinglePlayer.src.EntityComponentSystem.Components.ControlComponent import ControlComponent
from SinglePlayer.src.EntityComponentSystem.Components.DynamicsComponent import DynamicsComponent
from SinglePlayer.src.EntityComponentSystem.Components.PositionComponent import PositionComponent
from SinglePlayer.src.EntityComponentSystem.Components.ShootingComponent import ShootingComponent
from SinglePlayer.src.EntityComponentSystem.System.System import System
from SinglePlayer.src.KeyListener import KeyListener


class WeaponSystem(System):
    def __init__(self, entity_manager, entity_factory):
        super().__init__(entity_manager)
        self.entity_factory = entity_factory
        self.key_listener = KeyListener.get_instance()
        self.shot_sound = pygame.mixer.Sound(os.path.join('assets/sounds/', 'shot.mp3'))
        self.shot_sound.set_volume(0.2)

    def update(self, dt):
        entities = self.entity_manager.get_entities(ShootingComponent())

        for entity in entities:
            shot_comp = self.entity_manager.get_component(ShootingComponent(), entity)
            pos_comp = self.entity_manager.get_component(PositionComponent(), entity)
            dyn_comp = self.entity_manager.get_component(DynamicsComponent(), entity)
            con_comp = self.entity_manager.get_component(ControlComponent(), entity)

            if pos_comp and dyn_comp:
                shot = 0
                mine = 0
                if con_comp.id == 0:
                    shot = pygame.K_KP0
                    mine = pygame.K_KP1
                elif con_comp.id == 1:
                    shot = pygame.K_SPACE
                    mine = pygame.K_f
                else:
                    print("Wrong id in shooting system, program exit")
                    exit(0)
                if self.key_listener.is_pressed(shot):
                    time_since_last_shot = (get_time() * 1e-9) - shot_comp.last_time_shot
                    if time_since_last_shot > shot_comp.reload_time:
                        # inaccuracy mechanism
                        shot_angle = 0
                        if dyn_comp.vel.length() > 0:
                            max_angle = 2 / (math.pi * 2)
                            shot_angle = (random.random() * max_angle) - (max_angle / 2)
                        bullet_orient = pos_comp.orient.rotate(shot_angle)
                        self.entity_factory.create_bullet(pos_comp.pos.add(pos_comp.orient.scale(95)), bullet_orient,
                                                          shot_comp.bullet_speed, entity)
                        pygame.mixer.Sound.play(self.shot_sound)
                        shot_comp.last_time_shot = get_time() * 1e-9

                if self.key_listener.is_pressed(mine):
                    time_since_last_mine = (get_time() * 1e-9) - shot_comp.last_time_mine
                    if time_since_last_mine > shot_comp.reload_mine_time:
                        self.entity_factory.create_mine(pos_comp.pos, entity)
                        pygame.mixer.Sound.play(self.shot_sound)
                        shot_comp.last_time_mine = get_time() * 1e-9
