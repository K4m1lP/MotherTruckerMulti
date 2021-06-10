import pygame

from time import time_ns as get_time

from AdminPaanel.Events import Events
from AdminPaanel.Scenes.BattlesViewScene import BattlesViewScene
from AdminPaanel.Scenes.DocScene import DocScene
from AdminPaanel.Scenes.LoginScene import LoginScene
from AdminPaanel.Scenes.MapScene import MapScene
from AdminPaanel.Scenes.MenuScene import MenuScene
from AdminPaanel.Scenes.UserViewScene import UsersViewScene
from settings import SCR_HEIGHT, SCR_WIDTH


if __name__ == '__main__':
    pygame.init()
    game_window = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
    pygame.display.set_caption("MotherTracker-AdminPanel")
    should_close = False
    dt = 1 / 60
    end_time = 0
    start_time = get_time()
    current_scene = LoginScene(game_window)
    events_manager = Events.get_instance()
    while not should_close:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or events_manager.exit_event:
                should_close = True
        current_scene.draw(events)
        pygame.display.update()
        game_window.fill((120, 110, 100))
        change = events_manager.get_scene_change()
        if change:
            if change == "menu":
                current_scene = MenuScene(game_window)
            if change == "map":
                current_scene = MapScene(game_window)
            if change == "doc":
                current_scene = DocScene(game_window)
            if change == "login":
                current_scene = LoginScene(game_window)
            if change == "maps_view":
                current_scene = MapsViewScene(game_window)
            if change == "stats_view":
                current_scene = StatsViewScene(game_window)
            if change == "users_view":
                current_scene = UsersViewScene(game_window)
            if change == "battles_view":
                current_scene = BattlesViewScene(game_window)

        end_time = get_time()
        dt = (end_time - start_time) * 1e-9
        start_time = get_time()
    pygame.display.quit()
    pygame.quit()
    quit()


'''
Add / delete map
Documents
    Battles
    Users
    Stats
    Maps
'''