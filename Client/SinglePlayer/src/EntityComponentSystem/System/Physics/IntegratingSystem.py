from SinglePlayer.src.EntityComponentSystem.Components.DynamicsComponent import DynamicsComponent
from SinglePlayer.src.EntityComponentSystem.Components.HitboxComponent import HitboxComponent
from SinglePlayer.src.EntityComponentSystem.Components.PositionComponent import PositionComponent
from SinglePlayer.src.EntityComponentSystem.System.System import System
from SinglePlayer.src.utils.Vec2d import Vec2d

TOLERANCE = 2


class IntegratingSystem(System):
    def __init__(self, entity_manager):
        super().__init__(entity_manager)

    def update(self, dt):
        entities = self.entity_manager.get_entities(DynamicsComponent())
        for entity in entities:
            dynamics_comp = self.entity_manager.get_component(DynamicsComponent(), entity)
            pos_comp = self.entity_manager.get_component(PositionComponent(), entity)

            # acceleration
            acc = dynamics_comp.force.scale(dynamics_comp.inverse_mass)

            # velocity
            dynamics_comp.vel = dynamics_comp.vel.add(acc.scale(dt))
            if dynamics_comp.vel.length() < TOLERANCE and acc.length() < TOLERANCE:
                dynamics_comp.vel = Vec2d(0, 0)

            # position
            pos_comp.pos = pos_comp.pos.add(dynamics_comp.vel.scale(dt))
            hb_comp = self.entity_manager.get_component(HitboxComponent(), entity)
            if hb_comp:
                hb_comp.is_dirty = True

            # reset resultant force in component
            dynamics_comp.force = Vec2d(0, 0)
