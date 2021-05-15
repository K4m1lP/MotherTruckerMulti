import pygame
from time import time_ns as get_time

from EntityComponentSystem.System.Events.Events import Events
from Main.Client import Client
from Main.LoginScene import LoginScene
from Main.settings import SCR_HEIGHT, SCR_WIDTH, CONNECTED
from Main.KeyListener import KeyListener
from Main.GameplayScene import GameplayScene

if __name__ == '__main__':





    if CONNECTED:
        current_scene = LoginScene(game_window)
    else:
        current_scene = GameplayScene(game_window)
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
        event = events.get_scene()
        if event and event == "GameplayScene":
            current_scene = GameplayScene(game_window)
        if event and event == "LoginScene":
            current_scene = LoginScene(game_window)
    pygame.quit()
    quit()
