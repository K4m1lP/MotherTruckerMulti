from SinglePlayer.src.EntityComponentSystem.System.Physics.CollisionDetectionSystem import CollisionDetectionSystem
from SinglePlayer.src.EntityComponentSystem.System.Physics.CollisionResolveSystem import CollisionResolveSystem
from SinglePlayer.src.EntityComponentSystem.System.Physics.ControlSystem import ControlSystem
from SinglePlayer.src.EntityComponentSystem.System.Physics.HitboxSystem import HitboxSystem
from SinglePlayer.src.EntityComponentSystem.System.Physics.IntegratingSystem import IntegratingSystem
from SinglePlayer.src.EntityComponentSystem.System.Physics.ResistancesSystem import ResistancesSystem
from SinglePlayer.src.EntityComponentSystem.System.System import System


class PhysicsSystem(System):
    def __init__(self, entity_manager, entity_factory):
        super().__init__(entity_manager)
        self.entity_factory = entity_factory
        self.integrating_sys = IntegratingSystem(entity_manager)
        self.collision_det_sys = CollisionDetectionSystem(entity_manager)
        self.collision_res_sys = CollisionResolveSystem(entity_manager, self.entity_factory)
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
