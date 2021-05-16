from copy import deepcopy
from math import inf

from EntityComponentSystem.Components.DynamicsComponent import DynamicsComponent
from EntityComponentSystem.Components.HitboxComponent import HitboxComponent
from EntityComponentSystem.Components.PositionComponent import PositionComponent
from EntityComponentSystem.System.System import System
from EntityComponentSystem.Vec2d import Vec2d


class CollisionSystem(System):
    def __init__(self, entity_manager):
        super().__init__(entity_manager)

    def _test_sat(self, ent1, ent2):
        hb = [self.entity_manager.get_component_of_class(HitboxComponent(), ent1),
              self.entity_manager.get_component_of_class(HitboxComponent(), ent2)]
        pos_c = [self.entity_manager.get_component_of_class(PositionComponent(), ent1),
                 self.entity_manager.get_component_of_class(PositionComponent(), ent2)]
        dyn = [self.entity_manager.get_component_of_class(DynamicsComponent(), ent1),
               self.entity_manager.get_component_of_class(DynamicsComponent(), ent2)]
        inv_masses = [dyn[0].inverse_mass, dyn[1].inverse_mass]
        polys = [hb[0].transformed_vertices, hb[1].transformed_vertices]

        pen_deepness = inf
        pen = Vec2d(0, 0)
        for p in range(len(polys)):  # for both polygons..
            for edge in range(len(polys[p])):  # for each edge..

                # apply separated axis theorem
                edge_vec = polys[p][(edge + 1) % len(polys[p])].add(polys[p][edge].scale((-1)))
                perp_to_edge_vec = edge_vec.get_perp()
                perp_to_edge_vec.normalize()
                norm_to_the_edge = perp_to_edge_vec

                min_p1 = inf
                min_p2 = inf
                max_p1 = -inf
                max_p2 = -inf

                for point in polys[0]:  # for each point of polygon 1
                    min_p1 = min(min_p1, norm_to_the_edge.dot(point))
                    max_p1 = max(max_p1, norm_to_the_edge.dot(point))

                for point in polys[1]:  # for each point of polyon 2
                    min_p2 = min(min_p2, norm_to_the_edge.dot(point))
                    max_p2 = max(max_p2, norm_to_the_edge.dot(point))

                if min(max_p1, max_p2) - max(min_p1, min_p2) < pen_deepness:
                    # store potential deepness and direction of penetration
                    pen_deepness = min(max_p1, max_p2) - max(min_p1, min_p2)
                    pen = norm_to_the_edge

                if not ((max_p1 >= min_p2 and min_p1 <= max_p2) or (max_p2 >= min_p1 and min_p2 <= max_p1)):
                    return False

        # COLLISION OCCURRED, STATICALLY RESOLVING BY DISPLACING
        if inv_masses[0] > inv_masses[1]:  # first is lighter
            dyn[0].vel = dyn[0].vel.add(pen.scale(pen_deepness))
        elif inv_masses[1] > 0:
            dyn[1].vel = dyn[1].vel.add(pen.scale(-pen_deepness))

        return True

    def _test_diag(self, ent1, ent2):
        hb = [self.entity_manager.get_component_of_class(HitboxComponent(), ent1),
              self.entity_manager.get_component_of_class(HitboxComponent(), ent2)]
        pos = [self.entity_manager.get_component_of_class(PositionComponent(), ent1),
               self.entity_manager.get_component_of_class(PositionComponent(), ent2)]
        dyn = [self.entity_manager.get_component_of_class(DynamicsComponent(), ent1),
               self.entity_manager.get_component_of_class(DynamicsComponent(), ent2)]
        inv_masses = [dyn[0].inverse_mass, dyn[1].inverse_mass]
        centers = [pos[0].pos, pos[1].pos]
        polys = [hb[0].transformed_vertices, hb[1].transformed_vertices]

        for p in range(2):  # for both polygons...
            poly1 = deepcopy(polys[p])
            poly2 = deepcopy(polys[(p + 1) % 2])
            pos1 = centers[p]
            inv_mass1 = inv_masses[p]
            inv_mass2 = inv_masses[(p + 1) % 2]

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
                if inv_mass1 > inv_mass2:  # first is lighter
                    pos[p].pos = pos[p].pos.add(pen.scale(-1))
                    hb[p].is_dirty = True
                elif inv_mass2 > 0:
                    pos[(p + 1) % 2].pos = pos[(p + 1) % 2].pos.add(pen)
                    hb[(p + 1) % 2].is_dirty = True
                return True

            return False

    def _test_aabb(self, ent1, ent2):
        hb = [self.entity_manager.get_component_of_class(HitboxComponent(), ent1),
              self.entity_manager.get_component_of_class(HitboxComponent(), ent2)]
        up1 = up2 = right1 = right2 = inf
        down1 = down2 = left1 = left2 = -inf
        for p in hb[0].transformed_vertices:
            up1 = max(up1, p.y)
            right1 = max(right1, p.x)
            down1 = min(down1, p.y)
            left1 = min(left1, p.x)
        for p in hb[1].transformed_vertices:
            up2 = max(up2, p.y)
            right2 = max(right2, p.x)
            down2 = min(down2, p.y)
            left2 = min(left2, p.x)
        if left1 < right2 and right1 > left2 and \
                down1 < up2 and up1 > down2:
            return True
        return False

    def update(self, dt):
        entities = self.entity_manager.get_all_entities_possessing_component_of_class(HitboxComponent())
        for ent in entities:
            hb_comp = self.entity_manager.get_component_of_class(HitboxComponent(), ent)
            hb_comp.overlap = False

        n = len(entities)

        for i in range(n):  # for all pairs of entities
            for j in range(i + 1, n):
                if self._test_diag(entities[i], entities[j]):
                    hb_comp2 = self.entity_manager.get_component_of_class(HitboxComponent(), entities[j])
                    hb_comp1 = self.entity_manager.get_component_of_class(HitboxComponent(), entities[i])
                    hb_comp1.overlap = True
                    hb_comp2.overlap = True
