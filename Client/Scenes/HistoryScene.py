import pygame_menu

from Scenes.Scene import Scene
from settings import SCR_WIDTH, SCR_HEIGHT


class HistoryScene(Scene):

    def __init__(self, window):
        super().__init__(window)
        self.menu = create_history_view(self.client, self.events)

    def draw(self, events):
        if self.menu.is_enabled():
            self.menu.update(events)
            self.menu.draw(self.window)


def create_history_view(client, events):
    history = client.get_history()
    menu = pygame_menu.Menu('Mother Trucker', SCR_WIDTH, SCR_HEIGHT, theme=pygame_menu.themes.THEME_DARK)
    for bat in history:
        bat_str = ""
        for prop in bat:
            bat_str += prop
            bat_str += " "
            bat_str += str(bat[prop])
            bat_str += " "
        menu.add.button(bat_str)
    st = "You are logged as: " + client.get_nick()
    menu.add.label(st).scale(0.5, 0.5)
    menu.add.button("Back", back_function, events)
    return menu

def back_function(events):
    events.add_scene_change("menu")
