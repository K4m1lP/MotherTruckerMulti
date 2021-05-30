from copy import deepcopy
from math import cos, sin

from SinglePlayer.src.EntityComponentSystem.Components.HitboxComponent import HitboxComponent
from SinglePlayer.src.EntityComponentSystem.Components.PositionComponent import PositionComponent
from SinglePlayer.src.EntityComponentSystem.System.System import System
from SinglePlayer.src.utils.Vec2d import Vec2d


class HitboxSystem(System):
    """
    System is responsible for iterating over all entities that has a hitbox component
    and checking if it is dirty (has just moved or turned), and updates position of all
    hitbox (polygon) vertices to be on an appropriate place, using the new position and angle.
    It uses standard transformation matrix for translation and rotation.
    """

    def __init__(self, entity_manager):
        super().__init__(entity_manager)

    def update(self, dt):
        entities = self.entity_manager.get_entities(HitboxComponent())

        for entity in entities:
            hb_comp = self.entity_manager.get_component(HitboxComponent(), entity)

            if hb_comp.is_dirty:
                pos_comp = self.entity_manager.get_component(PositionComponent(), entity)
                angle = pos_comp.orient.get_angle_normalnie()
                poly = deepcopy(hb_comp.vertices)
                pos = deepcopy(pos_comp.pos)

                for i in range(len(poly)):
                    p1 = poly[i]
                    hb_comp.transformed_vertices[i] = Vec2d(pos.x + p1.x * cos(angle) - p1.y * sin(angle),
                                                            pos.y + p1.x * sin(angle) + p1.y * cos(angle))
                hb_comp.is_dirty = False
