import os

from SinglePlayer.src.EntityComponentSystem.Managers.EntityFactory import EntityFactory
from SinglePlayer.src.EntityComponentSystem.Managers.EntityManager import EntityManager
from SinglePlayer.src.EntityComponentSystem.System.AnimationSystem import AnimationSystem
from SinglePlayer.src.EntityComponentSystem.System.Physics.PhysicsSystem import PhysicsSystem
from SinglePlayer.src.EntityComponentSystem.System.RenderSystem import RenderSystem
from SinglePlayer.src.EntityComponentSystem.System.WeaponSystem import WeaponSystem
from SinglePlayer.src.Scene import Scene
from settings import SCR_WIDTH, SCR_HEIGHT


class GameplayScene(Scene):
    def __init__(self, window):
        super().__init__(window)
        self.entity_manager = EntityManager()
        self.entity_factory = EntityFactory(self.entity_manager)
        self.systems = [
            PhysicsSystem(self.entity_manager, self.entity_factory),
            WeaponSystem(self.entity_manager, self.entity_factory),
            AnimationSystem(self.entity_manager),
            RenderSystem(self.entity_manager, window)
        ]

        self.initialize()

    def initialize(self):
        self.entity_factory.create_player(0, (int(SCR_WIDTH * 0.9), int(SCR_HEIGHT * 0.5)))  # arrows
        self.entity_factory.create_player(1, (int(SCR_WIDTH * 0.1), int(SCR_HEIGHT * 0.5)))  # wsad
        self.entity_factory.create_border_walls()
        self.entity_factory.create_obstacles_from_file('map1.txt')

    def update(self, dt):
        for system in self.systems:
            system.update(dt)
        print("FPS: {}".format(1/dt))
