from EntityComponentSystem.Components.HealthComponent import HealthComponent
from EntityComponentSystem.Components.DynamicsComponent import DynamicsComponent
from EntityComponentSystem.Components.PositionComponent import PositionComponent
from EntityComponentSystem.Components.RenderComponent import RenderComponent


class Entity:

    def __init__(self, my_id, entity_manager):
        self.my_id = my_id
        self.entity_manager = entity_manager

    def move(self):
        return self.entity_manager.get_omponent_of_class(DynamicsComponent(), self.my_id)

    def health(self):
        return self.entity_manager.get_omponent_of_class(HealthComponent(), self.my_id)

    def position(self):
        return self.entity_manager.get_omponent_of_class(PositionComponent(), self.my_id)

    def render(self):
        return self.entity_manager.get_omponent_of_class(RenderComponent(), self.my_id)
