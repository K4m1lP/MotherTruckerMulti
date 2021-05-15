from EntityComponentSystem.System.Physics.CollisionSystem import CollisionSystem
from EntityComponentSystem.System.Physics.ControlSystem import ControlSystem
from EntityComponentSystem.System.Physics.HitboxSystem import HitboxSystem
from EntityComponentSystem.System.Physics.IntegratingSystem import IntegratingSystem
from EntityComponentSystem.System.Physics.ResistancesSystem import ResistancesSystem
from EntityComponentSystem.System.System import System


class PhysicsSystem(System):
    def __init__(self, entity_manager):
        super().__init__(entity_manager)
        self.integrating_sys = IntegratingSystem(entity_manager)
        self.collision_sys = CollisionSystem(entity_manager)
        self.control_sys = ControlSystem(entity_manager)
        self.resistances_sys = ResistancesSystem(entity_manager)
        self.hitbox_sys = HitboxSystem(entity_manager)

    def update(self, dt):
        self.hitbox_sys.update(dt)

        # force generating systems
        self.collision_sys.update(dt)

        self.control_sys.update(dt)

        self.resistances_sys.update(dt)

        # integration
        self.integrating_sys.update(dt)
