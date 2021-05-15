from EntityComponentSystem.Components.DynamicsComponent import DynamicsComponent
from EntityComponentSystem.Components.PositionComponent import PositionComponent
from EntityComponentSystem.System.System import System

DRAG = 0.0001
GROUND_FRICTION = 60


class ResistancesSystem(System):
    def __init__(self, entity_manager):
        super().__init__(entity_manager)

    def update(self, dt):
        entities = self.entity_manager.get_all_entities_possessing_component_of_class(DynamicsComponent())

        for entity in entities:

            dynamics_comp = self.entity_manager.get_component_of_class(DynamicsComponent(), entity)
            pos_comp = self.entity_manager.get_component_of_class(PositionComponent(), entity)

            if not pos_comp:
                continue

            vel = dynamics_comp.vel

            # air drag
            drag_force = vel.scale((-1) * DRAG * vel.length())
            dynamics_comp.force = dynamics_comp.force.add(drag_force)

            # ground friction
            if pos_comp.z == 0:  # if touches the ground
                friction_force = vel.scale((-1) * GROUND_FRICTION)
                dynamics_comp.force = dynamics_comp.force.add(friction_force)
