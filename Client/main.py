import pygame
import network
from time import time_ns as get_time
from event_manager import EventManager
from scenes.account_scene import AccountScene
from scenes.change_scene import ChangeScene
from scenes.game_over_scene import GameOverScene
from scenes.history_scene import HistoryScene
from scenes.login_scene import LoginScene
from scenes.menu_scene import MenuScene
from scenes.multi_game_scene import MultiGameScene
from scenes.server_scene import ServerScene
from scenes.setting_scene import SettingScene
from scenes.single_game_scene import SingleGameScene
from scenes.single_or_multi_scene import SingleOrMultiScene
from scenes.stats_scene import StatsScene
from scenes.waiting_scene import WaitingScene

from settings import SCR_HEIGHT, SCR_WIDTH


client = network.Client()
DISCONNECT_MSG = "!DISCONNECT"


def switch_scene():
    if change == "menu":
        return MenuScene(game_window)
    if change == "waiting_scene":
        return WaitingScene(game_window)
    if change == "game":
        return MultiGameScene(game_window)
    if change == "login":
        return LoginScene(game_window)
    if change == "account":
        return AccountScene(game_window)
    if change == "stats":
        return StatsScene(game_window)
    if change == "history":
        return HistoryScene(game_window)
    if change == "settings":
        return SettingScene(game_window)
    if change == "server_scene":
        return ServerScene(game_window)
    if change == "single_or_multi_scene":
        return SingleOrMultiScene(game_window)
    if change == "change_pass":
        return ChangeScene(game_window)
    if change == "game_over_scene":
        return GameOverScene(game_window)
    if change == "single_menu":
        return SingleGameScene(game_window)


if __name__ == '__main__':
    # init display
    pygame.init()
    game_window = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
    pygame.display.set_caption("MotherTrucker")

    # init closing conditions and time calculation
    should_close = False
    dt = 1 / 60
    end_time = 0
    start_time = get_time()

    # init first scene
    current_scene = SingleOrMultiScene(game_window)
    events_manager = EventManager.get_instance()

    # main game loop
    while not should_close:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or events_manager.exit_event:
                client.close_connection()
                should_close = True

        current_scene.draw(events)
        pygame.display.update()
        game_window.fill((120, 110, 100))

        change = events_manager.get_scene_change()
        if change:
            current_scene = switch_scene()

        end_time = get_time()
        dt = (end_time - start_time) * 1e-9
        start_time = get_time()

    pygame.display.quit()
    pygame.quit()
    quit()
