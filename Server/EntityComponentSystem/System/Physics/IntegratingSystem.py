from EntityComponentSystem.Components.DynamicsComponent import DynamicsComponent
from EntityComponentSystem.Components.HitboxComponent import HitboxComponent
from EntityComponentSystem.Components.PositionComponent import PositionComponent
from EntityComponentSystem.System.System import System
from utils.Vec2d import Vec2d

TOLERANCE = 2


class IntegratingSystem(System):
    def __init__(self, entity_manager):
        super().__init__(entity_manager)

    def update(self, dt):
        entities = self.entity_manager.get_all_entities_possessing_component_of_class(DynamicsComponent())
        for entity in entities:
            dynamics_comp = self.entity_manager.get_component_of_class(DynamicsComponent(), entity)
            pos_comp = self.entity_manager.get_component_of_class(PositionComponent(), entity)

            # acceleration
            acc = dynamics_comp.force.scale(dynamics_comp.inverse_mass)

            # velocity
            dynamics_comp.vel = dynamics_comp.vel.add(acc.scale(dt))
            if dynamics_comp.vel.length() < TOLERANCE and acc.length() < TOLERANCE:
                dynamics_comp.vel = Vec2d(0, 0)

            # position
            pos_comp.pos = pos_comp.pos.add(dynamics_comp.vel.scale(dt))
            hb_comp = self.entity_manager.get_component_of_class(HitboxComponent(), entity)
            hb_comp.is_dirty = True

            # reset resultant force in component
            dynamics_comp.force = Vec2d(0, 0)
