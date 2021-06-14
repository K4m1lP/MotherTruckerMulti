import os

import pygame

from scenes.scene import Scene
from settings import SCR_WIDTH, SCR_HEIGHT


class WaitingScene(Scene):
    def __init__(self, window):
        super().__init__(window)
        self.waiting_img_name = 'waiting.jpg'
        self.waiting_img_path_name = 'assets/images/other/'

    def draw(self, events):
        self.window.fill((40, 41, 35))
        img = pygame.image.load(os.path.join(self.waiting_img_path_name,
                                             self.waiting_img_name)).convert_alpha()
        self.window.blit(img, (SCR_WIDTH / 2 - (img.get_width() / 2), SCR_HEIGHT / 2 - (img.get_height() / 2)))
        second_player = self.client.is_second_connected()
        if second_player:
            self.event_manager.add_scene_change("game")

