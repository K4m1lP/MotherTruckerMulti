import pygame_menu

from scenes.scene import Scene
from settings import SCR_WIDTH, SCR_HEIGHT


class SingleOrMultiScene(Scene):
    def __init__(self, window):
        super().__init__(window)
        self.menu = create_single_or_multi_view(self.event_manager)

    def draw(self, events):
        if self.menu.is_enabled():
            self.menu.update(events)
            self.menu.draw(self.window)


def create_single_or_multi_view(events):
    menu = pygame_menu.Menu('Mother Trucker', SCR_WIDTH, SCR_HEIGHT, theme=pygame_menu.themes.THEME_DARK)
    menu.add.button('Single', single_function, events)
    menu.add.button('Multi', multi_function, events)
    menu.add.button('Quit', exit_fun, events)
    return menu


def single_function(events):
    events.add_scene_change("single_menu")


def multi_function(events):
    events.add_scene_change("server_scene")


def exit_fun(events):
    events.exit_event = True
