import pygame_menu

from scenes.scene import Scene
from settings import SCR_WIDTH, SCR_HEIGHT


class MenuScene(Scene):

    def __init__(self, window):
        super().__init__(window)
        self.menu = create_menu_view(self.client, self.event_manager)

    def draw(self, events):
        if self.menu.is_enabled():
            self.menu.update(events)
            self.menu.draw(self.window)


def create_menu_view(client, events):
    menu = pygame_menu.Menu('Mother Trucker', SCR_WIDTH, SCR_HEIGHT, theme=pygame_menu.themes.THEME_DARK)
    menu.add.button('Play', play_function, events, client)
    menu.add.button('My account', account_function, events)
    menu.add.button('My stats', stats_function, events)
    menu.add.button('My battle history', history_function, events)
    menu.add.button('Settings', settings_function, events)
    menu.add.button('Log out', logout_function, client, events)
    menu.add.button('Quit', exit_fun, events)
    st = "You are logged as: " + str(client.is_log)
    menu.add.label(st).scale(0.5, 0.5)
    return menu


def play_function(events, client):
    client.i_want_to_play()
    events.add_scene_change("waiting_scene")


def account_function(events):
    events.add_scene_change("account")


def stats_function(events):
    events.add_scene_change("stats")


def history_function(events):
    events.add_scene_change("history")


def settings_function(events):
    events.add_scene_change("settings")


def logout_function(client, events):
    client.logout()
    events.add_scene_change("login")


def exit_fun(events):
    events.exit_event = True
