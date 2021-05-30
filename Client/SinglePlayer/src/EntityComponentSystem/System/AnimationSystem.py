import os

import pygame

from time import time_ns as get_time

from SinglePlayer.src.EntityComponentSystem.Components.AnimationComponent import AnimationComponent
from SinglePlayer.src.EntityComponentSystem.Components.RenderComponent import RenderComponent
from SinglePlayer.src.EntityComponentSystem.System.System import System


class AnimationSystem(System):
    def __init__(self, entity_manager):
        super().__init__(entity_manager)

    def update(self, dt):
        entities = self.entity_manager.get_entities(AnimationComponent())

        for ent in entities:
            anim_comp = self.entity_manager.get_component(AnimationComponent(), ent)
            rend_comp = self.entity_manager.get_component(RenderComponent(), ent)

            if anim_comp:
                if anim_comp and rend_comp:
                    # if it's time to change texture:
                    if (get_time() - anim_comp.last_time_changed) > anim_comp.change_time:
                        anim_comp.last_time_changed = get_time()
                        # take next img of animation
                        anim_comp.curr_img_idx += 1
                        # if we run out of imgs delete entity totally
                        if anim_comp.curr_img_idx == anim_comp.img_num:
                            if anim_comp.img_name == 'explosion':
                                self.entity_manager.remove_entity(ent)
                            else:
                                anim_comp.curr_img_idx = -1
                            break
                        # else change render component img
                        else:
                            rend_comp.img_name = anim_comp.img_name + '{}'.format(anim_comp.curr_img_idx) + '.png'
                            rend_comp.ready = True
