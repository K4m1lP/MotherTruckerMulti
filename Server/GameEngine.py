from EntityComponentSystem.Entity.EntityManager import EntityManager
from EntityComponentSystem.Entity.EntityFactory import EntityFactory
from EntityComponentSystem.System.Physics.PhysicsSystem import PhysicsSystem
from EntityComponentSystem.System.ShootingSystem import ShootingSystem


class GameEngine:
    def __init__(self, window):
        super().__init__(window)
        self.entity_manager = EntityManager()
        self.entity_factory = EntityFactory(self.entity_manager)
        self.systems = [
            PhysicsSystem(self.entity_manager),
            ShootingSystem(self.entity_manager, self.entity_factory)
        ]

        self.initialize()

    def initialize(self):
        game_map = self.entity_factory.create_background()
        player_tank = self.entity_factory.create_protagonist()
        walls = self.entity_factory.create_border_walls()
        self.entity_factory.create_obstacles()

    def move(self):
        pass

    def update(self, dt):
        for system in self.systems:
            system.update(dt)

    def get_list_for_player(self):
        pass

    def get_stats_from_round(self):
        pass