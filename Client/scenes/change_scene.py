import pygame_menu

from Scenes.scene import Scene
from settings import SCR_WIDTH, SCR_HEIGHT


class ChangeScene(Scene):
    def __init__(self, window):
        super().__init__(window)
        self.menu = create_change_view(self.client, self.event_manager)

    def draw(self, events):
        if self.menu.is_enabled():
            self.menu.update(events)
            self.menu.draw(self.window)


def create_change_view(client, events):
    menu = pygame_menu.Menu('Mother Trucker', SCR_WIDTH, SCR_HEIGHT, theme=pygame_menu.themes.THEME_DARK)
    nick_id = menu.add.text_input('Nick :', default='').get_id()
    password_id = menu.add.text_input('Password :', default='', password=True).get_id()
    new_nick_id = menu.add.text_input('New nick :', default='').get_id()
    new_password_id = menu.add.text_input('New password :', default='', password=True).get_id()
    menu.add.button('Save', change_function, menu, nick_id, password_id, new_nick_id, new_password_id, client, events)
    menu.add.button('Quit', exit_fun, events)
    return menu


def exit_fun(events):
    events.exit_event = True


def change_function(menu, nick_id, password_id, new_nick_id, new_password_id, client, events):
    nick = pygame_menu.Menu.get_widget(menu, widget_id=nick_id).get_value()
    password = pygame_menu.Menu.get_widget(menu, widget_id=password_id).get_value()
    new_nick = pygame_menu.Menu.get_widget(menu, widget_id=new_nick_id).get_value()
    new_password = pygame_menu.Menu.get_widget(menu, widget_id=new_password_id).get_value()
    cos = client.change_password(nick, password, new_nick, new_password)
    if cos:
        events.add_scene_change("menu")
