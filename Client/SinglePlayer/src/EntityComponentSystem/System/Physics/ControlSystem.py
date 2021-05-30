import pygame

from SinglePlayer.src.EntityComponentSystem.Components.ControlComponent import ControlComponent
from SinglePlayer.src.EntityComponentSystem.Components.DynamicsComponent import DynamicsComponent
from SinglePlayer.src.EntityComponentSystem.Components.HitboxComponent import HitboxComponent
from SinglePlayer.src.EntityComponentSystem.Components.PositionComponent import PositionComponent
from SinglePlayer.src.EntityComponentSystem.System.System import System
from SinglePlayer.src.KeyListener import KeyListener
from SinglePlayer.src.utils.Vec2d import Vec2d


class ControlSystem(System):
    def __init__(self, entity_manager):
        super().__init__(entity_manager)
        self.key_listener = KeyListener.get_instance()

    def update(self, dt):
        entities = self.entity_manager.get_entities(DynamicsComponent())

        for entity in entities:

            dynamics_comp = self.entity_manager.get_component(DynamicsComponent(), entity)
            pos_comp = self.entity_manager.get_component(PositionComponent(), entity)
            control_comp = self.entity_manager.get_component(ControlComponent(), entity)

            if not pos_comp and dynamics_comp:
                continue

            # player impact - engine force and rotating
            if control_comp:
                if control_comp.id == 0:
                    left = pygame.K_LEFT
                    right = pygame.K_RIGHT
                    forward = pygame.K_UP
                    backward = pygame.K_DOWN
                elif control_comp.id == 1:
                    left = pygame.K_a
                    right = pygame.K_d
                    forward = pygame.K_w
                    backward = pygame.K_s
                else:
                    print("Wrong player id!")
                    return

                angle_change_direction = 0
                if self.key_listener.is_pressed(right):
                    angle_change_direction += 1
                if self.key_listener.is_pressed(left):
                    angle_change_direction -= 1
                if angle_change_direction != 0:
                    pos_comp.orient.normalize()
                    pos_comp.orient = pos_comp.orient.rotate(angle_change_direction * control_comp.rotation_speed * dt)
                    hb_comp = self.entity_manager.get_component(HitboxComponent(), entity)
                    hb_comp.is_dirty = True

                engine_force = Vec2d(0, 0)
                if self.key_listener.is_pressed(forward):
                    engine_force = engine_force.add(pos_comp.orient.scale(control_comp.engine_acc_forward))
                if self.key_listener.is_pressed(backward):
                    engine_force = engine_force.add(pos_comp.orient.scale(control_comp.engine_acc_backward * (-1)))

                dynamics_comp.force = dynamics_comp.force.add(engine_force)
