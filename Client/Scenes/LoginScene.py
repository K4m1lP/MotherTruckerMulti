import pygame_menu

from Scenes.Scene import Scene
from settings import SCR_WIDTH, SCR_HEIGHT


class LoginScene(Scene):
    def __init__(self, window):
        super().__init__(window)
        self.menu = create_login_view(self.client, self.events)

    def draw(self, events):
        if self.menu.is_enabled():
            self.menu.update(events)
            self.menu.draw(self.window)


def create_login_view(client, events):
    menu = pygame_menu.Menu('Mother Trucker', SCR_WIDTH, SCR_HEIGHT, theme=pygame_menu.themes.THEME_DARK)
    nick_id = menu.add.text_input('Nick :', default='').get_id()
    password_id = menu.add.text_input('Password :', default='', password=True).get_id()
    menu.add.button('Login', login_function, menu, nick_id, password_id, client, events)
    menu.add.button('Sign up', signup_function, menu, nick_id, password_id, client, events)
    menu.add.button('Quit', exit_fun, events)
    return menu


def login_function(menu, nick_id, password_id, client, events):
    nick = pygame_menu.Menu.get_widget(menu, widget_id=nick_id).get_value()
    password = pygame_menu.Menu.get_widget(menu, widget_id=password_id).get_value()
    logged = client.login(nick, password)
    if logged:
        client.is_log = logged
        events.add_scene_change("menu")


def exit_fun(events):
    events.exit_event = True


def signup_function(menu, nick_id, password_id, client, events):
    nick = pygame_menu.Menu.get_widget(menu, widget_id=nick_id).get_value()
    password = pygame_menu.Menu.get_widget(menu, widget_id=password_id).get_value()
    cos = client.sign(nick, password)
    if cos:
        events.add_scene_change("login")