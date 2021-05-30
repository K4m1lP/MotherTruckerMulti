from copy import deepcopy
from math import inf
from math import hypot

from SinglePlayer.src.EntityComponentSystem.Components.DynamicsComponent import DynamicsComponent
from SinglePlayer.src.EntityComponentSystem.Components.HitboxComponent import HitboxComponent
from SinglePlayer.src.EntityComponentSystem.Components.PositionComponent import PositionComponent
from SinglePlayer.src.EntityComponentSystem.Managers.CollisionManager import CollisionManager, Collision
from SinglePlayer.src.EntityComponentSystem.System.System import System
from SinglePlayer.src.utils.Vec2d import Vec2d


class CollisionDetectionSystem(System):
    def __init__(self, entity_manager):
        super().__init__(entity_manager)
        self.collision_manager = CollisionManager.get_instance()

    def _test_diag(self, ent1, ent2):
        hb = [self.entity_manager.get_component(HitboxComponent(), ent1),
              self.entity_manager.get_component(HitboxComponent(), ent2)]
        pos = [self.entity_manager.get_component(PositionComponent(), ent1),
               self.entity_manager.get_component(PositionComponent(), ent2)]
        centers = [pos[0].pos, pos[1].pos]
        polys = [hb[0].transformed_vertices, hb[1].transformed_vertices]

        for p in range(2):  # for both polygons...
            poly1 = deepcopy(polys[p])
            poly2 = deepcopy(polys[(p + 1) % 2])
            pos1 = centers[p]

            # how much one polygon penetrated the other one
            pen = Vec2d(0, 0)

            for i in range(len(poly1)):  # check "diagonals" of poly1...
                # diagonal - line segment from center to vertex
                d1 = pos1
                d2 = poly1[i]

                for j in range(len(poly2)):  # against edges of poly2
                    # edge - line segment from ith vertex to ith+1 vertex
                    e1 = poly2[j]
                    e2 = poly2[(j + 1) % len(poly2)]

                    # calculate penetration deepness
                    h = (e2.x - e1.x) * (d1.y - d2.y) - (d1.x - d2.x) * (e2.y - e1.y)
                    t1 = ((e1.y - e2.y) * (d1.x - e1.x) + (e2.x - e1.x) * (d1.y - e1.y)) / h
                    t2 = ((d1.y - d2.y) * (d1.x - e1.x) + (d2.x - d1.x) * (d1.y - e1.y)) / h

                    if 0 <= t1 <= 1 and 0 <= t2 <= 1:
                        pen.x += (1 - t1) * (d2.x - d1.x)
                        pen.y += (1 - t1) * (d2.y - d1.y)

            if pen.length() > 0:
                self.collision_manager.add_collision(Collision(ent1, ent2, pen.length(), pen))
                return True

            return False

    def _test_static(self, ent1, ent2):
        dyn = [self.entity_manager.get_component(DynamicsComponent(), ent1),
               self.entity_manager.get_component(DynamicsComponent(), ent2)]
        # don't care about static obstacles
        if dyn[0].inverse_mass == 0 and dyn[1].inverse_mass == 0:
            return False
        return True

    def _test_aabb(self, ent1, ent2):
        tr1 = self.entity_manager.get_component(HitboxComponent(), ent1).transformed_vertices
        tr2 = self.entity_manager.get_component(HitboxComponent(), ent2).transformed_vertices
        up1 = up2 = right1 = right2 = 1e9
        down1 = down2 = left1 = left2 = -1e9
        for p in tr1:
            up1 = max(up1, p.y)
            right1 = max(right1, p.x)
            down1 = min(down1, p.y)
            left1 = min(left1, p.x)
        for p in tr2:
            up2 = max(up2, p.y)
            right2 = max(right2, p.x)
            down2 = min(down2, p.y)
            left2 = min(left2, p.x)
        if left1 < right2 and right1 > left2 and down1 < up2 and up1 > down2:
            return True
        return False

    def update(self, dt):
        entities = self.entity_manager.get_entities(HitboxComponent())
        for ent in entities:
            hb_comp = self.entity_manager.get_component(HitboxComponent(), ent)
            hb_comp.overlap = False

        n = len(entities)

        for i in range(n):  # for all pairs of entities
            for j in range(i + 1, n):
                ent1 = entities[i]
                ent2 = entities[j]
                # initial tests
                if self._test_static(ent1, ent2) and self._test_aabb(ent1, ent2):
                    # pixel perfect test
                    if self._test_diag(ent1, ent2):
                        hb_comp2 = self.entity_manager.get_component(HitboxComponent(), entities[j])
                        hb_comp1 = self.entity_manager.get_component(HitboxComponent(), entities[i])
                        hb_comp1.overlap = True
                        hb_comp2.overlap = True
