import pygame
import Network

from time import time_ns as get_time

from Events import Events
from Scenes.AccountScene import AccountScene
from Scenes.ChangeScene import ChangeScene
from Scenes.GameOverScene import GameOverScene
from Scenes.GameScene import GameScene
from Scenes.HistoryScene import HistoryScene
from Scenes.LoginScene import LoginScene
from Scenes.MenuScene import MenuScene
from Scenes.ServerScene import ServerScene
from Scenes.SettingScene import SettingScene
from Scenes.SingleOrMultiScene import SingleOrMultiScene
from Scenes.StatsScene import StatsScene
from Scenes.WaittingScene import WaitingScene

from settings import SCR_HEIGHT, SCR_WIDTH
client = Network.Client()
DISCONNECT_MSG = "!DISCONNECT"


if __name__ == '__main__':
    pygame.init()
    game_window = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
    pygame.display.set_caption("MotherTracker")
    should_close = False
    dt = 1 / 60
    end_time = 0
    start_time = get_time()
    current_scene = SingleOrMultiScene(game_window)
    events_manager = Events.get_instance()
    while not should_close:
        game_window.fill((255, 200, 255))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or events_manager.exit_event:
                client.close_connection()
                should_close = True
        current_scene.draw(events)
        # print("FPS: {}".format(1 / dt))
        pygame.display.update()
        change = events_manager.get_scene_change()
        if change:
            if change == "menu":
                current_scene = MenuScene(game_window)
            if change == "waiting_scene":
                current_scene = WaitingScene(game_window)
            if change == "game":
                current_scene = GameScene(game_window)
            if change == "login":
                current_scene = LoginScene(game_window)
            if change == "account":
                current_scene = AccountScene(game_window)
            if change == "stats":
                current_scene = StatsScene(game_window)
            if change == "history":
                current_scene = HistoryScene(game_window)
            if change == "settings":
                current_scene = SettingScene(game_window)
            if change == "server_scene":
                current_scene = ServerScene(game_window)
            if change == "single_or_multi_scene":
                current_scene = SingleOrMultiScene(game_window)
            if change == "change_pass":
                current_scene = ChangeScene(game_window)
            if change == "game_over_scene":
                current_scene = GameOverScene(game_window)
        end_time = get_time()
        dt = (end_time - start_time) * 1e-9
        start_time = get_time()
    pygame.display.quit()
    pygame.quit()
    quit()

# podpiecie single
# przygotowanie okien servera
# poprawa wyswietlania
# dokumentacja
