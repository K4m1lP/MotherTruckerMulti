import pygame_menu

from AdminPaanel.Scenes.Scene import Scene
from settings import SCR_WIDTH, SCR_HEIGHT, DATA_BASE

class UsersViewScene(Scene):
    def __init__(self, window):
        super().__init__(window)
        self.menu = create_history_view(self.client, self.events)

    def draw(self, events):
        if self.menu.is_enabled():
            self.menu.update(events)
            self.menu.draw(self.window)


def create_history_view(client, events):
    history = client.get_all_users()
    menu = pygame_menu.Menu('Mother Trucker', SCR_WIDTH, SCR_HEIGHT, theme=pygame_menu.themes.THEME_ORANGE)
    for bat in history:
        menu.add.button(bat)
    menu.add.button("Back", back_fun, events)
    return menu


def back_fun(events):
    events.add_scene_change("menu")
