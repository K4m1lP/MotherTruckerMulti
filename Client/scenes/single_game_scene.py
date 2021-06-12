import os

import pygame
import pygame_menu
from time import time_ns as get_time
from settings import SCR_HEIGHT, SCR_WIDTH
from Scenes.scene import Scene
from engine.game_engine import GameEngine
from utils import Player


class SingleGameScene(Scene):
    def __init__(self, window):
        super().__init__(window)
        self.player1_name = "player1"
        self.player2_name = "player2"
        self.game_keys = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE,
                          pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
                          pygame.K_KP0, pygame.K_KP1, pygame.K_f, pygame.K_ESCAPE,
                          pygame.K_TAB, pygame.K_e]
        self.pressed_keys = {}
        for key in self.game_keys:
            self.pressed_keys[key] = False
        self.prev_pressed_keys = {}
        for key in self.game_keys:
            self.prev_pressed_keys[key] = False
        self.images = {}
        self.gui_textures = {self.player1_name: [], self.player2_name: []}
        self.init_gui_textures()
        self.does_menu = False
        self.menu = pygame_menu.Menu(title="Game menu", height=250, width=500, theme=pygame_menu.themes.THEME_DARK)
        self.menu.add.button("Quit", exit_fun, self.event_manager)
        self.engine = GameEngine(Player(self.player1_name), Player(self.player2_name))
        self.end_time_frame_ended = get_time()
        self.fps_sys = FpsRenderSystem(window)
        self.end_time = None

    def draw(self, events):
        dt = (get_time() - self.end_time_frame_ended) * 1e-9
        self.end_time_frame_ended = get_time()
        self.get_keys(events)
        game_state = self.engine.update(dt, self.pressed_keys)

        if game_state.has_ended and self.end_time is None:
            self.end_time = get_time()
        if self.end_time and (get_time()-self.end_time) * 1e-9 >= 1:
            game_state.should_exit = True
            self.event_manager.add_scene_change("game_over_scene")
            self.event_manager.set_winner(game_state.winner)
            return

        self.render_all(game_state.to_render, dt)

        self.render_gui(game_state)

        if self.does_menu and not self.pressed_keys[pygame.K_TAB]:
            if self.menu.is_enabled():
                self.menu.update(events)
                self.menu.draw(self.window)

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

    def render_all(self, sprites, dt):
        sprites.sort(key=lambda s: s.z)
        if sprites:
            for sprite in sprites:
                x = sprite.pos.x
                y = sprite.pos.y
                # if new, save to ram not to access disc every frame
                image_name = sprite.img_name
                if image_name not in self.images and image_name != 'tile.png':
                    self.images[image_name] = pygame.image.load(os.path.join('assets/images/textures/', image_name)).convert_alpha()
                    if sprite.size and sprite.fixed_size:
                        self.images[image_name] = pygame.transform.scale(self.images[image_name], sprite.size)
                elif image_name == 'tile.png':
                    self.images[image_name] = pygame.image.load(os.path.join('assets/images/textures/', image_name)).convert_alpha()
                    self.images[image_name] = pygame.transform.scale(self.images[image_name], sprite.size)

                image = self.images[image_name]
                if sprite.size and not sprite.fixed_size:
                    image = pygame.transform.scale(image, sprite.size)
                if not sprite.fixed_orient:
                    image = pygame.transform.rotate(image, sprite.orient.to_angle_degrees())
                # render
                render_pos = (int(x - image.get_width() / 2), int(y - image.get_height() / 2))
                self.window.blit(image, render_pos)
        self.fps_sys.update(dt)

    def render_gui(self, game_state):
        if game_state:
            background1 = self.gui_textures[self.player1_name]
            self.window.blit(background1[0], background1[1])


    def init_gui_textures(self):
        def load_image(_path, name):
            return pygame.image.load(os.path.join(_path, name)).convert_alpha()

        _path = 'assets/images/textures/'

        self.gui_textures[self.player1_name] = [
            (load_image(_path, "gui_background.jpg"), (40, 40)),
            (load_image(_path, "tank0avatar.png"), (20, 25)),
            (load_image(_path, "bullet-icon-full.png"), (70, 35)),
            (load_image(_path, "bullet-icon-empty.jpg"), (70, 35)),
        ]
        self.gui_textures[self.player2_name] = [
            (load_image(_path, "gui_background.jpg"), (SCR_WIDTH-(40 + 300), 40)),
            (load_image(_path, "tank1avatar.png"), (20, 25)),
            (load_image(_path, "bullet-icon-full.png"), (70, 35)),
            (load_image(_path, "bullet-icon-empty.jpg"), (70, 35)),
        ]


def exit_fun(events):
    events.exit_event = True


class FpsRenderSystem:
    def __init__(self, window):
        self.window = window
        self.font_size = 50
        self.font = pygame.font.SysFont(None, self.font_size)
        self.color = (200, 140, 0)
        self.fps_counter_pos = (10, 10)
        self.fps_period = 1  # how often to refresh fps
        self.fps_time_left = 0
        self.fps_tmp_curr_val = 0

    def update(self, dt):

        if self.fps_time_left <= 0 and dt != 0:
            self.fps_tmp_curr_val = int(round(1 / dt, 0))
            self.fps_time_left = self.fps_period
        else:
            self.fps_time_left -= dt
        img = self.font.render(repr(self.fps_tmp_curr_val), True, self.color)
        self.window.blit(img, self.fps_counter_pos)