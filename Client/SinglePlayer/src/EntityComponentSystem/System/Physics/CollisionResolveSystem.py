import os

import pygame


from time import time_ns as get_time

from SinglePlayer.src.EntityComponentSystem.Components.DynamicsComponent import DynamicsComponent
from SinglePlayer.src.EntityComponentSystem.Components.HealthComponent import HealthComponent
from SinglePlayer.src.EntityComponentSystem.Components.HitComponent import HitComponent
from SinglePlayer.src.EntityComponentSystem.Components.HitboxComponent import HitboxComponent
from SinglePlayer.src.EntityComponentSystem.Components.PositionComponent import PositionComponent
from SinglePlayer.src.EntityComponentSystem.Managers.CollisionManager import CollisionManager
from SinglePlayer.src.EntityComponentSystem.System.System import System


class CollisionResolveSystem(System):
    def __init__(self, entity_manager, entity_factory):
        super().__init__(entity_manager)
        self.entity_factory = entity_factory
        self.collision_manager = CollisionManager.get_instance()
        self.hit_sound = pygame.mixer.Sound(os.path.join('assets/sounds/', 'hit.mp3'))
        self.hit_sound.set_volume(0.3)

    def update(self, dt):
        collisions = self.collision_manager.get_collisions()

        for col in collisions:
            ent1 = col.ent1
            ent2 = col.ent2
            hit_comp1 = self.entity_manager.get_component(HitComponent(), ent1)
            hit_comp2 = self.entity_manager.get_component(HitComponent(), ent2)
            health_comp1 = self.entity_manager.get_component(HealthComponent(), ent1)
            health_comp2 = self.entity_manager.get_component(HealthComponent(), ent2)
            pos_comp1 = self.entity_manager.get_component(PositionComponent(), ent1)
            pos_comp2 = self.entity_manager.get_component(PositionComponent(), ent2)

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
                    pygame.mixer.Sound.play(self.hit_sound)
                    self.entity_manager.remove_entity(ent1)
                    if health_comp2:
                        health_comp2.last_time_hit = get_time()
                        # ent2 has health, so it is being hit and loses health
                        if health_comp2.curr_hp - dmg <= 0:
                            health_comp2.curr_hp = 0
                            self.entity_factory.create_explosion(pos_comp2.pos, (200, 200))
                            pygame.mixer.Sound.play(self.hit_sound)
                            pygame.mixer.Sound.play(self.hit_sound)
                            pygame.mixer.Sound.play(self.hit_sound)
                            self.entity_manager.remove_entity(ent2)
                        else:
                            health_comp2.curr_hp -= dmg
                continue
            # check 2 against 1
            if hit_comp2:
                if (get_time() - hit_comp2.time_placed) > hit_comp2.activation_time:
                    dmg = hit_comp2.dmg
                    # ent2 is exploding
                    self.entity_factory.create_explosion(pos_comp2.pos)
                    pygame.mixer.Sound.play(self.hit_sound)
                    self.entity_manager.remove_entity(ent2)
                    if health_comp1:
                        health_comp1.last_time_hit = get_time()
                        # ent1 has health, so it is being hit and loses health
                        if health_comp1.curr_hp - dmg <= 0:
                            health_comp1.curr_hp = 0
                            self.entity_factory.create_explosion(pos_comp1.pos, (200, 200))
                            pygame.mixer.Sound.play(self.hit_sound)
                            pygame.mixer.Sound.play(self.hit_sound)
                            pygame.mixer.Sound.play(self.hit_sound)
                            self.entity_manager.remove_entity(ent1)
                        else:
                            health_comp1.curr_hp -= dmg
                continue

            # 2) CHECK FOR DISPLACING
            dyn_comp1 = self.entity_manager.get_component(DynamicsComponent(), ent1)
            dyn_comp2 = self.entity_manager.get_component(DynamicsComponent(), ent2)
            hb_comp1 = self.entity_manager.get_component(HitboxComponent(), ent1)
            hb_comp2 = self.entity_manager.get_component(HitboxComponent(), ent2)

            if dyn_comp1 and dyn_comp2 and hb_comp1 and hb_comp2 and pos_comp1 and pos_comp2:
                if dyn_comp1.inverse_mass > dyn_comp2.inverse_mass:  # first is lighter
                    pos_comp1.pos = pos_comp1.pos.add(col.pen_vec.scale(-1))
                    hb_comp1.is_dirty = True
                elif dyn_comp2.inverse_mass > 0:
                    pos_comp2.pos = pos_comp2.pos.add(col.pen_vec)
                    hb_comp2.is_dirty = True
