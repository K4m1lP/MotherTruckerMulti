import pygame

from EntityComponentSystem.Components.HealthComponent import HealthComponent
from EntityComponentSystem.Components.PositionComponent import PositionComponent
from EntityComponentSystem.Components.RenderComponent import RenderComponent
from EntityComponentSystem.System.System import System


class HealthSystem(System):

    def update(self, dt):
        entities = self.entity_manager.get_all_entities_possessing_component_of_class(HealthComponent())
        for entity in entities:
            health_component_obj_for_entity = self.entity_manager.get_component_of_class(HealthComponent(), entity)
            if not health_component_obj_for_entity.alive:
                return
            if health_component_obj_for_entity.max_hp == 0:
                return
            if health_component_obj_for_entity.cur_hp <= 0:
                # dopiero co umarł, zagraj melodie
                health_component_obj_for_entity.alive = False
                self.entity_manager.remove_entity(entity)

