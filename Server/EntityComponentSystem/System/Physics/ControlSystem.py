import pygame

from EntityComponentSystem.Components.ControlComponent import ControlComponent
from EntityComponentSystem.Components.DynamicsComponent import DynamicsComponent
from EntityComponentSystem.Components.HitboxComponent import HitboxComponent
from EntityComponentSystem.Components.PositionComponent import PositionComponent
from EntityComponentSystem.System.System import System

from EntityComponentSystem.Vec2d import Vec2d


class ControlSystem(System):
    def __init__(self, entity_manager):
        super().__init__(entity_manager)
        self.key_listener = KeyListener.get_instance()

    def update(self, dt):
        entities = self.entity_manager.get_all_entities_possessing_component_of_class(DynamicsComponent())

        for entity in entities:

            dynamics_comp = self.entity_manager.get_component_of_class(DynamicsComponent(), entity)
            pos_comp = self.entity_manager.get_component_of_class(PositionComponent(), entity)
            control_comp = self.entity_manager.get_component_of_class(ControlComponent(), entity)

            if not pos_comp and dynamics_comp:
                continue

            # player impact - engine force and rotating
            if control_comp:
                angle_change_direction = 0
                if self.key_listener.is_pressed(pygame.K_d):
                    angle_change_direction += 1
                if self.key_listener.is_pressed(pygame.K_a):
                    angle_change_direction -= 1
                if angle_change_direction != 0:
                    pos_comp.orient.normalize()
                    pos_comp.orient = pos_comp.orient.rotate(angle_change_direction * control_comp.rotation_speed * dt)
                    hb_comp = self.entity_manager.get_component_of_class(HitboxComponent(), entity)
                    hb_comp.is_dirty = True

                engine_force = Vec2d(0, 0)
                if self.key_listener.is_pressed(pygame.K_w):
                    engine_force = engine_force.add(pos_comp.orient.scale(control_comp.engine_acc_forward))
                if self.key_listener.is_pressed(pygame.K_s):
                    engine_force = engine_force.add(pos_comp.orient.scale(control_comp.engine_acc_backward * (-1)))

                dynamics_comp.force = dynamics_comp.force.add(engine_force)
