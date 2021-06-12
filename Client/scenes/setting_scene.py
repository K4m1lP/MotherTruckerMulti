import pygame_menu

from Scenes.scene import Scene
from settings import SCR_WIDTH, SCR_HEIGHT


class SettingScene(Scene):

    def __init__(self, window):
        super().__init__(window)
        self.menu = create_settings_view(self.client, self.event_manager)

    def draw(self, events):
        if self.menu.is_enabled():
            self.menu.update(events)
            self.menu.draw(self.window)


def create_settings_view(client, events):
    menu = pygame_menu.Menu('Mother Trucker', SCR_WIDTH, SCR_HEIGHT, theme=pygame_menu.themes.THEME_DARK)
    menu.add.button('Some option1')
    menu.add.button('Some option2')
    menu.add.button('Back', back_function, events)
    st = "You are logged as: " + client.get_nick()
    menu.add.label(st).scale(0.5, 0.5)
    return menu


def back_function(events):
    events.add_scene_change("menu")
