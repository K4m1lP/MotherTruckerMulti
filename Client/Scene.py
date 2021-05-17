import os
import pygame
import pygame_menu
from time import time_ns as get_time

from Events import Events
from Network import Client

from settings import SCR_HEIGHT, SCR_WIDTH


class Scene:
    def __init__(self, window):
        self.window = window
        self.client = Client.get_instance()
        self.events = Events.get_instance()


class GameScene(Scene):
    def __init__(self, window):
        super().__init__(window)
        self.client.unlock_socket()
        self.game_keys = [pygame.K_a, pygame.K_d, pygame.K_a, pygame.K_s, pygame.K_SPACE,
                          pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
                          pygame.K_KP0, pygame.K_KP1, pygame.K_f, pygame.K_w, pygame.K_ESCAPE,
                          pygame.K_TAB, pygame.K_e]
        self.prev_pressed_keys = {}
        for key in self.game_keys:
            self.prev_pressed_keys[key] = False
        self.pressed_keys = {}
        for key in self.game_keys:
            self.pressed_keys[key] = False
        self.obj = None
        self.images = {}
        self.does_menu = False
        self.menu = pygame_menu.Menu(title="Game menu", height=250, width=500, theme=pygame_menu.themes.THEME_DARK)
        self.menu.add.button("Quit", exit_fun, self.events)
        self.score_tab = pygame_menu.Menu(title="Score tab", height=250, width=500, theme=pygame_menu.themes.THEME_DARK)
        self.score_tab.add.label("Your hp: ")
        self.score_tab.add.label("Opponent hp: ")

    def draw(self, events):
        is_changed = self.get_keys(events)
        if is_changed:
            self.client.send_key(self.pressed_keys)

        obj_to_render = self.client.get_game_status()
        if obj_to_render:
            self.obj = obj_to_render
        if self.obj:
            self.render(self.obj)

        if self.does_menu and not self.pressed_keys[pygame.K_TAB]:
            s = pygame.Surface((1000, 500), pygame.SRCALPHA)
            s.fill((0, 0, 0, 128))
            self.window.blit(s, (0, 0))
            if self.menu.is_enabled():
                self.menu.update(events)
                self.menu.draw(self.window)

        if self.pressed_keys[pygame.K_TAB] and not self.does_menu:
            s = pygame.Surface((1000, 500), pygame.SRCALPHA)
            s.fill((0, 0, 0, 128))
            self.window.blit(s, (0, 0))
            if self.score_tab.is_enabled():
                self.score_tab.update(events)
                self.score_tab.draw(self.window)

    def get_keys(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                key = event.key
                if key in self.game_keys:
                    self.pressed_keys[key] = True
                    if key == pygame.K_ESCAPE and not self.prev_pressed_keys[key]:
                        self.does_menu = not self.does_menu
            elif event.type == pygame.KEYUP:
                key = event.key
                if key in self.game_keys:
                    self.pressed_keys[key] = False
        huj = False
        for code in self.prev_pressed_keys:
            if self.prev_pressed_keys[code] != self.pressed_keys[code]:
                huj = True
            self.prev_pressed_keys[code] = self.pressed_keys[code]
        return huj

    def render(self, to_render):
        to_render.sort(key=lambda s: s.z)
        if to_render:
            for sprite in to_render:
                x = sprite.pos.x
                y = sprite.pos.y
                # if new, save to ram not to access disc every frame
                image_name = sprite.img_name
                if image_name not in self.images:
                    self.images[image_name] = pygame.image.load(os.path.join('assets/images/textures/', image_name))
                    if sprite.size and sprite.fixed_size:
                        self.images[image_name] = pygame.transform.scale(self.images[image_name], sprite.size)

                image = self.images[image_name]
                if sprite.size and not sprite.fixed_size:
                    image = pygame.transform.scale(image, sprite.size)
                if not sprite.fixed_orient:
                    image = pygame.transform.rotate(image, sprite.orient.get_angle())
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
        self.client.unlock_socket()

    def draw(self, events):
        self.window.fill((40, 41, 35))
        gif = pygame.image.load("assets/waiting.gif").convert_alpha()
        self.window.blit(gif, (SCR_WIDTH / 2 - (gif.get_width() / 2), SCR_HEIGHT / 2 - (gif.get_height() / 2)))
        second_player = self.client.is_second_connected()
        if second_player:
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
    st = "You are logged as: " + client.is_log()
    menu.add.label(st).scale(0.5, 0.5)
    return menu


def create_stats_view(client):
    stats = client.get_stats()
    menu = pygame_menu.Menu('Mother Trucker', SCR_WIDTH, SCR_HEIGHT, theme=pygame_menu.themes.THEME_DARK)
    for i in stats:
        menu.add.button(i)
    st = "You are logged as: " + client.is_log()
    menu.add.label(st).scale(0.5, 0.5)
    return menu


def create_account_view(client, events):
    account = client.get_account()
    menu = pygame_menu.Menu('Mother Trucker', SCR_WIDTH, SCR_HEIGHT, theme=pygame_menu.themes.THEME_DARK)
    nick_str = "Your nick: " + account["nick"]
    menu.add.button(nick_str)
    menu.add.button('Back', back_function, events)
    return menu


def create_settings_view(client, events):
    menu = pygame_menu.Menu('Mother Trucker', SCR_WIDTH, SCR_HEIGHT, theme=pygame_menu.themes.THEME_DARK)
    menu.add.button('Some option1')
    menu.add.button('Some option2')
    menu.add.button('Back', back_function, events)
    st = "You are logged as: " + client.is_log()
    menu.add.label(st).scale(0.5, 0.5)
    return menu


def back_function(events):
    events.add_scene_change("menu")


def create_login_view(client, events):
    menu = pygame_menu.Menu('Mother Trucker', SCR_WIDTH, SCR_HEIGHT, theme=pygame_menu.themes.THEME_DARK)
    nick_id = menu.add.text_input('Nick :', default='').get_id()
    password_id = menu.add.text_input('Password :', default='', password=True).get_id()
    menu.add.button('Login', login_function, menu, nick_id, password_id, client, events)
    menu.add.button('Quit', exit_fun, events)
    return menu


def create_menu_view(client, events):
    menu = pygame_menu.Menu('Mother Trucker', SCR_WIDTH, SCR_HEIGHT, theme=pygame_menu.themes.THEME_DARK)
    menu.add.button('Play', play_function, events, client)
    menu.add.button('My account', account_function, events, client)
    menu.add.button('My stats', stats_function, events, client)
    menu.add.button('My battle history', history_function, events, client)
    menu.add.button('Settings', settings_function, events)
    menu.add.button('Log out', logout_function, client, events)
    menu.add.button('Quit', exit_fun, events)
    st = "You are logged as: " + client.is_log()
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


def exit_fun(events):
    events.exit_event = True
