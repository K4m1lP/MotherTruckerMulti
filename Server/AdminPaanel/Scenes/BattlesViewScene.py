import pygame_menu

from AdminPaanel.Scenes.Scene import Scene
from settings import SCR_WIDTH, SCR_HEIGHT, DATA_BASE

class BattlesViewScene(Scene):
    def __init__(self, window):
        super().__init__(window)
        self.menu = create_history_view(self.client, self.events)

    def draw(self, events):
        if self.menu.is_enabled():
            self.menu.update(events)
            self.menu.draw(self.window)


def create_history_view(client, events):
    history = client.get_all_battles()
    menu = pygame_menu.Menu('Mother Trucker', SCR_WIDTH, SCR_HEIGHT, theme=pygame_menu.themes.THEME_ORANGE)
    for bat in history:
        bat_str = ""
        for prop in bat:
            bat_str += prop
            bat_str += " "
            bat_str += str(bat[prop])
            bat_str += " "
        menu.add.button(bat_str)
    menu.add.button("Back", back_fun, events)
    return menu


def back_fun(events):
    events.add_scene_change("menu")
