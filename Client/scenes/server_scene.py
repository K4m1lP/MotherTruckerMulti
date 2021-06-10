import pygame_menu

from scenes.scene import Scene
from settings import SCR_WIDTH, SCR_HEIGHT


class ServerScene(Scene):
    def __init__(self, window):
        super().__init__(window)
        self.menu = create_server_view(self.client, self.events)

    def draw(self, events):
        if self.menu.is_enabled():
            self.menu.update(events)
            self.menu.draw(self.window)


def create_server_view(client, events):
    menu = pygame_menu.Menu('Mother Trucker', SCR_WIDTH, SCR_HEIGHT, theme=pygame_menu.themes.THEME_DARK)
    server_ip = menu.add.text_input('Server IP: ', default='').get_id()
    menu.add.button('Connect', server_function, menu, server_ip, client, events)
    menu.add.button('Back', back_function, events)
    menu.add.button('Quit', exit_fun, events)
    return menu


def server_function(menu, server_ip, client, events):
    ip = pygame_menu.Menu.get_widget(menu, widget_id=server_ip).get_value()
    if ip:
        client.connect(ip)
        if client.pos:
            events.add_scene_change("login")


def exit_fun(events):
    events.exit_event = True


def back_function(events):
    events.add_scene_change("single_or_multi_scene")
