import pygame_menu

from AdminPaanel.Scenes.Scene import Scene
from settings import SCR_WIDTH, SCR_HEIGHT


class MenuScene(Scene):

    def __init__(self, window):
        super().__init__(window)
        self.menu = create_menu_view(self.client, self.events)

    def draw(self, events):
        if self.menu.is_enabled():
            self.menu.update(events)
            self.menu.draw(self.window)


def create_menu_view(client, events):
    menu = pygame_menu.Menu('Mother Trucker Panel Admin', SCR_WIDTH, SCR_HEIGHT, theme=pygame_menu.themes.THEME_ORANGE)
    menu.add.button('Add / delete map', map_function, events, client)
    menu.add.button('Documents', doc_function, events)
    menu.add.button('Log out', logout_function, client, events)
    menu.add.button('Quit', exit_fun, events)
    st = "You are logged as: Admin"
    menu.add.label(st).scale(0.5, 0.5)
    return menu


def map_function(events, client):
    events.add_scene_change("map")


def doc_function(events):
    events.add_scene_change("doc")


def logout_function(client, events):
    client.logout()
    events.add_scene_change("login")


def exit_fun(events):
    events.exit_event = True
