import pygame_menu

from AdminPaanel.Scenes.Scene import Scene
from settings import SCR_WIDTH, SCR_HEIGHT, DATA_BASE

class MapScene(Scene):
    def __init__(self, window):
        super().__init__(window)
        self.menu = create_map_view(self.client, self.events)

    def draw(self, events):
        if self.menu.is_enabled():
            self.menu.update(events)
            self.menu.draw(self.window)


def create_map_view(client, events):
    menu = pygame_menu.Menu('Mother Trucker Maps', SCR_WIDTH, SCR_HEIGHT, theme=pygame_menu.themes.THEME_ORANGE)
    add_map_name = menu.add.text_input('Name of new map: ', default='').get_id()
    pos1 = menu.add.text_input('Position 1: ', default='').get_id()
    pos2 = menu.add.text_input('Position 2: ', default='').get_id()
    src = menu.add.text_input('Path name: ', default='').get_id()
    menu.add.button('Add', add_function, menu, add_map_name, pos1, pos2, src)

    map_to_delete = menu.add.text_input('Map to delete: ', default='', password=True).get_id()
    menu.add.button('Delete', rem_function, menu, map_to_delete, client, events)

    menu.add.button('Back', back_fun, events)
    return menu


def add_function(menu, add_map_name, pos1, pos2, src, client, events):
    add_map_name = pygame_menu.Menu.get_widget(menu, widget_id=add_map_name).get_value()
    pos1 = pygame_menu.Menu.get_widget(menu, widget_id=pos1).get_value()
    pos1.split(sep=",")
    pos2 = pygame_menu.Menu.get_widget(menu, widget_id=pos2).get_value()
    pos1.split(sep=",")
    src = pygame_menu.Menu.get_widget(menu, widget_id=src).get_value()
    if client.add_map(src, add_map_name, pos1, pos2):
        events.add_scene_change("menu")


def rem_function(menu, map_to_delete, client, events):
    add_map_name = pygame_menu.Menu.get_widget(menu, widget_id=map_to_delete).get_value()
    if client.delete_map(add_map_name):
        events.add_scene_change("menu")


def back_fun(events):
    events.add_scene_change("menu")

