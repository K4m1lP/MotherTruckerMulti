from engine.entities import EntityManager, EntityFactory
from engine.systems import PhysicsSystem, ShootingSystem, KeysUpdateSystem, GameStateSystem
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
        self.ph_sys = PhysicsSystem(self.entity_manager)
        self.sht_sys = ShootingSystem(self.entity_manager, self.entity_factory)
        self.state_sys = GameStateSystem(self.entity_manager)

        # some start game objects
        self.initialize()

    def update(self, dt, keys1, keys2):
        if keys1:
            self.player1.keys = keys1
        if keys2:
            self.player2.keys = keys2
        self.keys_sys.update(self.player1.keys, self.player2.keys)
        self.ph_sys.update(dt)
        self.sht_sys.update(dt)

        return self.state_sys.get_state(dt)

    def initialize(self):
        self.entity_factory.create_background()
        self.entity_factory.create_protagonist(self.player1, (int(SCR_WIDTH * 0.1), int(SCR_HEIGHT * 0.25)))
        self.entity_factory.create_protagonist(self.player2, (int(SCR_WIDTH * 0.1), int(SCR_HEIGHT * 0.75)))
        self.entity_factory.create_border_walls()
