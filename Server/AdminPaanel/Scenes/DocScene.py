import pygame_menu

from AdminPaanel.Scenes.Scene import Scene
from settings import SCR_WIDTH, SCR_HEIGHT, DATA_BASE

class DocScene(Scene):
    def __init__(self, window):
        super().__init__(window)
        self.menu = create_del_user_view(self.client, self.events)

    def draw(self, events):
        if self.menu.is_enabled():
            self.menu.update(events)
            self.menu.draw(self.window)


def create_del_user_view(client, events):
    menu = pygame_menu.Menu('Mother Trucker Documents', SCR_WIDTH, SCR_HEIGHT, theme=pygame_menu.themes.THEME_ORANGE)
    menu.add.button('Battles', battles_function, client, events)
    menu.add.button('Users', users_function, client, events)
    #menu.add.button('Stats', stats_function, client, events)
    #menu.add.button('Maps', maps_function, client, events)
    menu.add.button('Back', back_fun, events)
    return menu


def battles_function(client, events):
    events.add_scene_change("battles_view")


def users_function(client, events):
    events.add_scene_change("users_view")


def stats_function(client, events):
    events.add_scene_change("stats_view")


def maps_function(client, events):
    events.add_scene_change("maps_view")


def back_fun(events):
    events.add_scene_change("menu")
