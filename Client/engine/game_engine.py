from engine.entities import EntityManager, EntityFactory
from engine.systems import PhysicsSystem, WeaponSystem, KeysUpdateSystem, GameStateSystem, AnimationSystem
from settings import *


class GameEngine:
    def __init__(self, player1, player2):
        self.entity_manager = EntityManager()
        self.entity_factory = EntityFactory(self.entity_manager)
        # players:
        self.player1 = player1
        self.player2 = player2
        # systems:
        self.keys_sys = KeysUpdateSystem(self.entity_manager)
        self.ph_sys = PhysicsSystem(self.entity_manager, self.entity_factory)
        self.wpn_sys = WeaponSystem(self.entity_manager, self.entity_factory)
        self.anim_sys = AnimationSystem(self.entity_manager)
        self.state_sys = GameStateSystem(self.entity_manager)

        # some start game objects
        self.initialize()

    def update(self, dt, keys):
        self.keys_sys.update(keys)
        self.ph_sys.update(dt)
        self.wpn_sys.update(dt)
        self.anim_sys.update(dt)
        # print("FPS: {}".format(1 / dt))
        return self.state_sys.get_state(dt)

    def initialize(self):
        self.entity_factory.create_protagonist(self.player1)
        self.entity_factory.create_protagonist(self.player2)
        self.entity_factory.create_border_walls()
        # self.entity_factory.create_obstacles_from_file('map0.txt')
        self.entity_factory.create_default_obstacles()
