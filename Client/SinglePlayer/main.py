import os

import pygame
from time import time_ns as get_time

from SinglePlayer.src.GameplayScene import GameplayScene
from SinglePlayer.src.KeyListener import KeyListener
from settings import SCR_HEIGHT, SCR_WIDTH


if __name__ == '__main__':

    pygame.init()
    pygame.mixer.init()
    game_window = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
    pygame.display.set_caption("MotherTracker")
    key_listener = KeyListener()

    current_scene = GameplayScene(game_window)

    pygame.mixer.music.load(os.path.join('assets/sounds/', 'game_theme.ogg'))
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(-1)

    should_close = False
    dt = 1 / 60
    end = 0
    start = get_time()
    while not should_close:
        # listen to key presses
        should_close = key_listener.listen()

        # update all game logic
        current_scene.update(dt)

        # draw the graphics
        pygame.display.update()
        game_window.fill((0, 0, 0))

        # calculate time of the frame
        end = get_time()
        dt = (end - start) * 1e-9
        start = get_time()

    pygame.quit()
    quit()
