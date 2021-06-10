import pygame_menu

from AdminPaanel.Scenes.Scene import Scene
from settings import SCR_WIDTH, SCR_HEIGHT, DATA_BASE

class DelUserScene(Scene):
    def __init__(self, window):
        super().__init__(window)
        self.menu = create_del_user_view(self.client, self.events)

    def draw(self, events):
        if self.menu.is_enabled():
            self.menu.update(events)
            self.menu.draw(self.window)


def create_del_user_view(client, events):
    menu = pygame_menu.Menu('Mother Trucker', SCR_WIDTH, SCR_HEIGHT, theme=pygame_menu.themes.THEME_ORANGE)
    nick_id = menu.add.text_input('Nick of user to remove: ', default='').get_id()
    menu.add.button('Remove', remove_function, menu, nick_id, client, events)
    menu.add.button('Back', back_fun, events)
    return menu


def remove_function(menu, nick_id, client, events):
    nick = pygame_menu.Menu.get_widget(menu, widget_id=nick_id).get_value()
    client.remove_user(nick)
    events.add_scene_change("menu")


def back_fun(events):
    events.add_scene_change("menu")
