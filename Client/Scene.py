import os

import pygame
import pygame_menu
from time import time_ns as get_time

from Events import Events
from Network import Client

SCR_WIDTH, SCR_HEIGHT = 1000, 500


class Scene:
    def __init__(self, window):
        self.window = window
        self.client = Client.get_instance()
        self.events = Events.get_instance()


class GameScene(Scene):
    def __init__(self, window):
        super().__init__(window)

    def draw(self, events):
        obj_to_render = self.client.send_key(pygame.key.get_pressed())
        if obj_to_render:
            self.render(obj_to_render)

    def render(self, to_render):
        for sprite in to_render:
            x = sprite.pos.x
            y = sprite.pos.y
            # don't show objects that are outside camera view
            if not (-100 <= x <= SCR_WIDTH + 100 and -100 <= y <= SCR_HEIGHT + 100):
                return
            image_name = sprite.img
            image = pygame.image.load(os.path.join('assets/images/textures/', image_name))
            size = sprite.size
            angle = sprite.orient.get_angle()
            # scale and rotate image
            image = pygame.transform.rotate(pygame.transform.scale(image, size), angle)
            # render
            render_pos = (int(x - image.get_width() / 2), int(y - image.get_height() / 2))
            self.window.blit(image, render_pos)



class LoginScene(Scene):
    def __init__(self, window):
        super().__init__(window)
        self.menu = create_login_view(self.client, self.events)

    def draw(self, events):
        if self.menu.is_enabled():
            self.menu.update(events)
            self.menu.draw(self.window)


class WaitingScene(Scene):
    def __init__(self, window):
        super().__init__(window)
        print("elo waiting scene")

    def draw(self, events):
        self.window.fill((40, 41, 35))
        gif = pygame.image.load("assets/waiting.gif").convert_alpha()
        self.window.blit(gif, (SCR_WIDTH / 2 - (gif.get_width() / 2), SCR_HEIGHT / 2 - (gif.get_height() / 2)))
        print("czytamy czy jest drugi ", get_time())
        second_player = self.client.is_second_connected()
        print(second_player)
        if second_player:
            print("Mozna zaczynac jest drugi do gry")
            self.events.add_scene_change("game")


class MenuScene(Scene):

    def __init__(self, window):
        super().__init__(window)
        self.menu = create_menu_view(self.client, self.events)

    def draw(self, events):
        if self.menu.is_enabled():
            self.menu.update(events)
            self.menu.draw(self.window)


class SettingScene(Scene):

    def __init__(self, window):
        super().__init__(window)
        self.menu = create_settings_view(self.client, self.events)

    def draw(self, events):
        if self.menu.is_enabled():
            self.menu.update(events)
            self.menu.draw(self.window)


class AccountScene(Scene):

    def __init__(self, window):
        super().__init__(window)
        self.menu = create_account_view(self.client, self.events)

    def draw(self, events):
        if self.menu.is_enabled():
            self.menu.update(events)
            self.menu.draw(self.window)


class StatsScene(Scene):

    def __init__(self, window):
        super().__init__(window)
        self.menu = create_stats_view(self.events)

    def draw(self, events):
        if self.menu.is_enabled():
            self.menu.update(events)
            self.menu.draw(self.window)


class HistoryScene(Scene):

    def __init__(self, window):
        super().__init__(window)
        self.menu = create_history_view(self.events)

    def draw(self, events):
        if self.menu.is_enabled():
            self.menu.update(events)
            self.menu.draw(self.window)


def login_function(menu, nick_id, password_id, client, events):
    if client.pos is not None:
        nick = pygame_menu.Menu.get_widget(menu, widget_id=nick_id).get_value()
        password = pygame_menu.Menu.get_widget(menu, widget_id=password_id).get_value()
        client.login(nick, password)
        if client.is_log():
            events.add_scene_change("menu")
def create_history_view(client):
    history = client.get_history()
    menu = pygame_menu.Menu('Mother Trucker', SCR_WIDTH, SCR_HEIGHT, theme=pygame_menu.themes.THEME_DARK)
    for i in history:
        menu.add.button(i)
    st = "You are logged as: "+client.is_log()
    menu.add.label(st).scale(0.5, 0.5)
    return menu
def create_stats_view(client):
    stats = client.get_stats()
    menu = pygame_menu.Menu('Mother Trucker', SCR_WIDTH, SCR_HEIGHT, theme=pygame_menu.themes.THEME_DARK)
    for i in stats:
        menu.add.button(i)
    st = "You are logged as: "+client.is_log()
    menu.add.label(st).scale(0.5, 0.5)
    return menu
def create_account_view(client, events):
    account = client.get_account()
    menu = pygame_menu.Menu('Mother Trucker', SCR_WIDTH, SCR_HEIGHT, theme=pygame_menu.themes.THEME_DARK)
    nick_str = "Your nick: "+account["nick"]
    menu.add.button(nick_str)
    menu.add.button('Back', back_function, events)
    return menu
def create_settings_view(client, events):
    menu = pygame_menu.Menu('Mother Trucker', SCR_WIDTH, SCR_HEIGHT, theme=pygame_menu.themes.THEME_DARK)
    menu.add.button('Some option1')
    menu.add.button('Some option2')
    menu.add.button('Back', back_function, events)
    st = "You are logged as: "+client.is_log()
    menu.add.label(st).scale(0.5, 0.5)
    return menu
def back_function(events):
    events.add_scene_change("menu")
def create_login_view(client, events):
    menu = pygame_menu.Menu('Mother Trucker', SCR_WIDTH, SCR_HEIGHT, theme=pygame_menu.themes.THEME_DARK)
    nick_id = menu.add.text_input('Nick :', default='').get_id()
    password_id = menu.add.text_input('Password :', default='', password=True).get_id()
    menu.add.button('Login', login_function, menu, nick_id, password_id, client, events)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    return menu
def create_menu_view(client, events):
    menu = pygame_menu.Menu('Mother Trucker', SCR_WIDTH, SCR_HEIGHT, theme=pygame_menu.themes.THEME_DARK)
    menu.add.button('Play', play_function, events, client)
    menu.add.button('My account', account_function, events, client)
    menu.add.button('My stats', stats_function, events, client)
    menu.add.button('My battle history', history_function, events, client)
    menu.add.button('Settings', settings_function, events)
    menu.add.button('Log out', logout_function, client, events)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    st = "You are logged as: "+client.is_log()
    menu.add.label(st).scale(0.5, 0.5)
    return menu
def settings_function(events):
    events.add_scene_change("settings")
def account_function(events):
    events.add_scene_change("account")
def stats_function(events):
    events.add_scene_change("stats")
def history_function(events):
    events.add_scene_change("history")
def logout_function(client, events):
    client.logout()
    events.add_scene_change("login")
def play_function(events, client):
    client.i_want_to_play()
    events.add_scene_change("waiting_scene")
