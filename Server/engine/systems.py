import math
import random
from copy import deepcopy
from math import cos, sin, inf


import pygame


from engine.components import *
from engine.entities import Collision, CollisionManager
from utils import GameState, Sprite


class PhysicsSystem:
    def __init__(self, entity_manager, entity_factory):
        self.entity_manager = entity_manager
        self.integrating_sys = IntegratingSystem(entity_manager)
        self.collision_det_sys = CollisionDetectionSystem(entity_manager)
        self.collision_res_sys = CollisionResolveSystem(entity_manager, entity_factory)
        self.control_sys = ControlSystem(entity_manager)
        self.resistances_sys = ResistancesSystem(entity_manager)
        self.hitbox_sys = HitboxSystem(entity_manager)

    def update(self, dt):
        self.hitbox_sys.update(dt)

        # force generating systems
        self.collision_det_sys.update(dt)
        self.collision_res_sys.update(dt)

        self.control_sys.update(dt)

        self.resistances_sys.update(dt)

        # integration
        self.integrating_sys.update(dt)


class IntegratingSystem:
    def __init__(self, entity_manager):
        self.entity_manager = entity_manager
        self.tolerance = 2

    def update(self, dt):
        entities = self.entity_manager.get_all_entities_possessing_component_of_class(DynamicsComponent())
        for entity in entities:
            dynamics_comp = self.entity_manager.get_component_of_class(DynamicsComponent(), entity)
            pos_comp = self.entity_manager.get_component_of_class(PositionComponent(), entity)

            # acceleration
            acc = dynamics_comp.force * dynamics_comp.inverse_mass

            # velocity
            dynamics_comp.vel = dynamics_comp.vel + acc * dt
            if dynamics_comp.vel.length() < self.tolerance and acc.length() < self.tolerance:
                dynamics_comp.vel = Vec2d(0, 0)

            # position
            pos_comp.pos = pos_comp.pos + dynamics_comp.vel * dt
            hb_comp = self.entity_manager.get_component_of_class(HitboxComponent(), entity)
            hb_comp.is_dirty = True

            # reset resultant force in component
            dynamics_comp.force = Vec2d(0, 0)


class ControlSystem:
    def __init__(self, entity_manager):
        self.entity_manager = entity_manager

    def update(self, dt):
        entities = self.entity_manager.get_all_entities_possessing_component_of_class(DynamicsComponent())

        for entity in entities:

            dynamics_comp = self.entity_manager.get_component_of_class(DynamicsComponent(), entity)
            pos_comp = self.entity_manager.get_component_of_class(PositionComponent(), entity)
            control_comp = self.entity_manager.get_component_of_class(ControlComponent(), entity)

            if not pos_comp and dynamics_comp:
                continue

            # player impact - engine force and rotating
            if control_comp and control_comp.player.keys:
                angle_change_direction = 0
                if control_comp.player.keys[pygame.K_d]:
                    angle_change_direction += 1
                if control_comp.player.keys[pygame.K_a]:
                    angle_change_direction -= 1
                if angle_change_direction != 0:
                    pos_comp.orient.normalize()
                    pos_comp.orient = pos_comp.orient.rotate(angle_change_direction * control_comp.rotation_speed * dt)
                    hb_comp = self.entity_manager.get_component_of_class(HitboxComponent(), entity)
                    hb_comp.is_dirty = True

                engine_force = Vec2d(0, 0)
                if control_comp.player.keys[pygame.K_w]:
                    engine_force = engine_force + pos_comp.orient * control_comp.engine_acc_forward
                if control_comp.player.keys[pygame.K_s]:
                    engine_force = engine_force + pos_comp.orient * control_comp.engine_acc_backward * (-1)

                dynamics_comp.force = dynamics_comp.force + engine_force


class HitboxSystem:
    """
    System is responsible for iterating over all entities that has a hitbox component
    and checking if it is dirty (has just moved or turned), and updates position of all
    hitbox (polygon) vertices to be on an appropriate place, using the new position and angle.
    It uses standard transformation matrix for translation and rotation.
    """

    def __init__(self, entity_manager):
        self.entity_manager = entity_manager

    def update(self, dt):
        entities = self.entity_manager.get_all_entities_possessing_component_of_class(HitboxComponent())

        for entity in entities:
            hb_comp = self.entity_manager.get_component_of_class(HitboxComponent(), entity)

            if hb_comp.is_dirty:
                pos_comp = self.entity_manager.get_component_of_class(PositionComponent(), entity)
                angle = pos_comp.orient.to_angle_radians()
                poly = deepcopy(hb_comp.vertices)
                pos = deepcopy(pos_comp.pos)

                for i in range(len(poly)):
                    p1 = poly[i]
                    hb_comp.transformed_vertices[i] = Vec2d(pos.x + p1.x * cos(angle) - p1.y * sin(angle),
                                                            pos.y + p1.x * sin(angle) + p1.y * cos(angle))
                hb_comp.is_dirty = False


class CollisionDetectionSystem:
    def __init__(self, entity_manager):
        self.entity_manager = entity_manager
        self.collision_manager = CollisionManager.get_instance()

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
                edge_vec = polys[p][(edge + 1) % len(polys[p])] + (polys[p][edge] * (-1))
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
            pos_c[0].pos = pos_c[0].pos + pen * pen_deepness
        elif inv_masses[1] > 0:
            pos_c[1].pos = pos_c[1].pos + pen * -pen_deepness

        return True

    def _test_diag(self, ent1, ent2):
        hb = [self.entity_manager.get_component_of_class(HitboxComponent(), ent1),
              self.entity_manager.get_component_of_class(HitboxComponent(), ent2)]
        pos = [self.entity_manager.get_component_of_class(PositionComponent(), ent1),
               self.entity_manager.get_component_of_class(PositionComponent(), ent2)]
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


class CollisionResolveSystem:
    def __init__(self, entity_manager, entity_factory):
        self.entity_manager = entity_manager
        self.entity_factory = entity_factory
        self.collision_manager = CollisionManager.get_instance()

    def update(self, dt):
        collisions = self.collision_manager.get_collisions()

        for col in collisions:
            ent1 = col.ent1
            ent2 = col.ent2
            hit_comp1 = self.entity_manager.get_component_of_class(HitComponent(), ent1)
            hit_comp2 = self.entity_manager.get_component_of_class(HitComponent(), ent2)
            health_comp1 = self.entity_manager.get_component_of_class(HealthComponent(), ent1)
            health_comp2 = self.entity_manager.get_component_of_class(HealthComponent(), ent2)
            pos_comp1 = self.entity_manager.get_component_of_class(PositionComponent(), ent1)
            pos_comp2 = self.entity_manager.get_component_of_class(PositionComponent(), ent2)

            # 1) CHECK FOR HITTING AND EXPLODING
            # I assume that entity can't have both HitComp and HealthComp
            if hit_comp1 and health_comp1:
                raise Exception("Entity {} has both hit and health component!".format(ent1))

            if hit_comp2 and health_comp2:
                raise Exception("Entity {} has both hit and health component!".format(ent2))

            # check 1 against 2
            if hit_comp1:
                if (get_time() - hit_comp1.time_placed) > hit_comp1.activation_time:
                    dmg = hit_comp1.dmg
                    # ent1 is exploding
                    self.entity_factory.create_explosion(pos_comp1.pos)
                    self.entity_manager.remove_entity(ent1)
                    if health_comp2:
                        health_comp2.last_time_hit = get_time()
                        # ent2 has health, so it is being hit and loses health
                        if health_comp2.curr_hp - dmg <= 0:
                            health_comp2.curr_hp = 0
                            self.entity_factory.create_explosion(pos_comp2.pos, (200, 200))
                            self.entity_manager.delete_component(RenderComponent(), ent2)
                        else:
                            health_comp2.curr_hp -= dmg
                continue
            # check 2 against 1
            if hit_comp2:
                if (get_time() - hit_comp2.time_placed) > hit_comp2.activation_time:
                    dmg = hit_comp2.dmg
                    # ent2 is exploding
                    self.entity_factory.create_explosion(pos_comp2.pos)
                    self.entity_manager.remove_entity(ent2)
                    if health_comp1:
                        health_comp1.last_time_hit = get_time()
                        # ent1 has health, so it is being hit and loses health
                        if health_comp1.curr_hp - dmg <= 0:
                            health_comp1.curr_hp = 0
                            self.entity_factory.create_explosion(pos_comp1.pos, (200, 200))
                            self.entity_manager.delete_component(RenderComponent(), ent1)
                        else:
                            health_comp1.curr_hp -= dmg
                continue

            # 2) CHECK FOR DISPLACING
            dyn_comp1 = self.entity_manager.get_component_of_class(DynamicsComponent(), ent1)
            dyn_comp2 = self.entity_manager.get_component_of_class(DynamicsComponent(), ent2)
            hb_comp1 = self.entity_manager.get_component_of_class(HitboxComponent(), ent1)
            hb_comp2 = self.entity_manager.get_component_of_class(HitboxComponent(), ent2)

            if dyn_comp1 and dyn_comp2 and hb_comp1 and hb_comp2 and pos_comp1 and pos_comp2:
                if dyn_comp1.inverse_mass > dyn_comp2.inverse_mass:  # first is lighter
                    pos_comp1.pos = pos_comp1.pos + (col.pen_vec.__mul__(-1))
                    hb_comp1.is_dirty = True
                elif dyn_comp2.inverse_mass > 0:
                    pos_comp2.pos = pos_comp2.pos + col.pen_vec
                    hb_comp2.is_dirty = True


class ResistancesSystem:
    def __init__(self, entity_manager):
        self.entity_manager = entity_manager
        self.drag = float(1e-4)
        self.ground_friction = 60

    def update(self, dt):
        entities = self.entity_manager.get_all_entities_possessing_component_of_class(DynamicsComponent())

        for entity in entities:

            dynamics_comp = self.entity_manager.get_component_of_class(DynamicsComponent(), entity)
            pos_comp = self.entity_manager.get_component_of_class(PositionComponent(), entity)

            if not pos_comp:
                continue

            vel = dynamics_comp.vel

            # air drag
            drag_force = vel * -1 * self.drag * vel.length()
            dynamics_comp.force = dynamics_comp.force + drag_force

            # ground friction
            if pos_comp.z <= 1:  # if touches the ground
                friction_force = vel * -1 * self.ground_friction
                dynamics_comp.force = dynamics_comp.force + friction_force


class WeaponSystem:
    def __init__(self, entity_manager, entity_factory):
        self.entity_manager = entity_manager
        self.entity_factory = entity_factory
        # self.shot_sound = pygame.mixer.Sound(os.path.join('assets/sounds/', 'shot.mp3'))
        # self.shot_sound.set_volume(0.2)

    def update(self, dt):
        entities = self.entity_manager.get_all_entities_possessing_component_of_class(ShootingComponent())

        for entity in entities:
            shot_comp = self.entity_manager.get_component_of_class(ShootingComponent(), entity)
            pos_comp = self.entity_manager.get_component_of_class(PositionComponent(), entity)
            dyn_comp = self.entity_manager.get_component_of_class(DynamicsComponent(), entity)
            con_comp = self.entity_manager.get_component_of_class(ControlComponent(), entity)

            if pos_comp and dyn_comp and con_comp and con_comp.player.keys:
                if con_comp.player.keys[pygame.K_SPACE]:
                    time_since_last_shot = (get_time() * 1e-9) - shot_comp.last_time_shot
                    if time_since_last_shot > shot_comp.reload_time:
                        # inaccuracy mechanism
                        shot_angle = 0
                        if dyn_comp.vel.length() > 0:
                            max_angle = 2 / (math.pi * 2)
                            shot_angle = (random.random() * max_angle) - (max_angle / 2)
                        bullet_orient = pos_comp.orient.rotate(shot_angle)
                        self.entity_factory.create_bullet(pos_comp.pos + pos_comp.orient * 95, bullet_orient,
                                                          shot_comp.bullet_speed, entity)
                        # pygame.mixer.Sound.play(self.shot_sound)
                        shot_comp.last_time_shot = get_time() * 1e-9

                if con_comp.player.keys[pygame.K_f]:
                    time_since_last_mine = (get_time() * 1e-9) - shot_comp.last_time_mine
                    if time_since_last_mine > shot_comp.reload_mine_time:
                        self.entity_factory.create_mine(pos_comp.pos, entity)
                        # pygame.mixer.Sound.play(self.shot_sound)
                        shot_comp.last_time_mine = get_time() * 1e-9


class AnimationSystem:
    def __init__(self, entity_manager):
        self.entity_manager = entity_manager

    def update(self, dt):
        entities = self.entity_manager.get_all_entities_possessing_component_of_class(AnimationComponent())

        for ent in entities:
            anim_comp = self.entity_manager.get_component_of_class(AnimationComponent(), ent)
            rend_comp = self.entity_manager.get_component_of_class(RenderComponent(), ent)

            if anim_comp:
                if anim_comp and rend_comp:
                    # if it's time to change texture:
                    if (get_time() - anim_comp.last_time_changed) > anim_comp.change_time:
                        anim_comp.last_time_changed = get_time()
                        # take next img of animation
                        anim_comp.curr_img_idx += 1
                        # if we run out of imgs delete entity totally
                        if anim_comp.curr_img_idx == anim_comp.img_num:
                            self.entity_manager.remove_entity(ent)
                            break
                        # else change render component img
                        else:
                            rend_comp.img_name = anim_comp.img_name + '{}'.format(anim_comp.curr_img_idx) + '.png'
                            rend_comp.ready = True


# multiplayer...
class KeysUpdateSystem:
    def __init__(self, entity_manager):
        self.entity_manager = entity_manager

    def update(self, keys1, keys2):
        entities = self.entity_manager.get_all_entities_possessing_component_of_class(ControlComponent())

        for ent in entities:
            control_comp = self.entity_manager.get_component_of_class(ControlComponent(), ent)
            if control_comp.player.id == 0:
                control_comp.player.keys = keys1
            elif control_comp.player.id == 1:
                control_comp.player.keys = keys2
            else:
                print("Error: KeysUpdateSystem: wrong player id!")
                exit(1)


class GameStateSystem:
    def __init__(self, entity_manager):
        self.entity_manager = entity_manager
        self.state = GameState()

    def get_state(self, dt):
        # update objects to render
        self.state.to_render = []
        entities = self.entity_manager.get_all_entities_possessing_component_of_class(RenderComponent())
        for ent in entities:
            rend_comp = self.entity_manager.get_component_of_class(RenderComponent(), ent)
            pos_comp = self.entity_manager.get_component_of_class(PositionComponent(), ent)
            if pos_comp and rend_comp:
                self.state.to_render.append(Sprite(pos_comp, rend_comp))

        # update frame time
        self.state.frame_time = dt

        self.check_for_endgame()

        # return ready state (for clients)
        return deepcopy(self.state)

    def check_for_endgame(self):
        entities = self.entity_manager.get_all_entities_possessing_component_of_class(ControlComponent())
        for ent in entities:
            control_comp = self.entity_manager.get_component_of_class(ControlComponent(), ent)
            health_comp = self.entity_manager.get_component_of_class(HealthComponent(), ent)
            if health_comp:
                if health_comp.curr_hp <= 0:
                    self.state.has_ended = True
                    self.state.winner = control_comp.player.nick
