import pygame_menu

from Scenes.Scene import Scene
from settings import SCR_HEIGHT, SCR_WIDTH


class AccountScene(Scene):

    def __init__(self, window):
        super().__init__(window)
        self.menu = create_account_view(self.client, self.events)

    def draw(self, events):
        if self.menu.is_enabled():
            self.menu.update(events)
            self.menu.draw(self.window)


def create_account_view(client, events):
    account = client.get_nick()
    menu = pygame_menu.Menu('Mother Trucker', SCR_WIDTH, SCR_HEIGHT, theme=pygame_menu.themes.THEME_DARK)
    nick_str = "Your nick: " + account
    menu.add.button(nick_str)
    menu.add.button("Change password or nick", change_password_or_nick, client, events)
    menu.add.button('Back', back_function, events)
    return menu


def change_password_or_nick(client, event):
    event.add_scene_change("change_pass")


def back_function(events):
    events.add_scene_change("menu")

