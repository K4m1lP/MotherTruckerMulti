import os

import pygame
import pygame_menu
from time import time_ns as get_time
from settings import SCR_HEIGHT, SCR_WIDTH, GAME_KEYS
from scenes.scene import Scene
from engine.game_engine import GameEngine
from utils import Player


class SingleGameScene(Scene):
    def __init__(self, window):
        super().__init__(window)
        self.player1_name = "Dark Conqueror"
        self.player2_name = "Knight of Light"
        self.game_keys = GAME_KEYS
        self.pressed_keys = {}
        for key in self.game_keys: self.pressed_keys[key] = False
        self.prev_pressed_keys = {}
        for key in self.game_keys: self.prev_pressed_keys[key] = False
        self.images = {}
        self.gui_textures = {self.player1_name: [], self.player2_name: []}
        self.init_gui_textures()
        self.player_name_font_size = 30
        self.player_name_font = pygame.font.SysFont(None, self.player_name_font_size)
        self.does_menu = False
        self.menu = pygame_menu.Menu(title="Game menu", height=250, width=500, theme=pygame_menu.themes.THEME_DARK)
        self.menu.add.button("Quit", switch_to_menu, self.event_manager)
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
            if game_state.looser == self.player1_name:
                self.event_manager.set_winner(self.player2_name)
            else:
                self.event_manager.set_winner(self.player1_name)
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
        for player in [self.player1_name, self.player2_name]:
            gui_elements = self.gui_textures[player]
            bg_pos = gui_elements[0][1]
            # background
            self.window.blit(*gui_elements[0])
            # tank-avatar
            self.window.blit(gui_elements[1][0], (gui_elements[1][1][0] + bg_pos[0],
                                                  gui_elements[1][1][1] + bg_pos[1]))
            # bullet-icon
            if game_state.shot_ready[player]:
                self.window.blit(gui_elements[2][0], (gui_elements[2][1][0] + bg_pos[0],
                                                      gui_elements[2][1][1] + bg_pos[1]))
            else:
                self.window.blit(gui_elements[3][0], (gui_elements[3][1][0] + bg_pos[0],
                                                      gui_elements[3][1][1] + bg_pos[1]))
            # hp full bar
            length = 170
            thickness = 60
            start_offset = (105, 70)
            start_point = [bg_pos[0] + start_offset[0], bg_pos[1] + start_offset[1]]
            end_point = [bg_pos[0] + start_offset[0] + length, bg_pos[1] + start_offset[1]]
            pygame.draw.line(self.window, pygame.color.Color(190, 150, 0), start_point, end_point, thickness)
            # hp current bar
            if game_state.curr_hp[player] == 0: continue
            hp_normalized = game_state.curr_hp[player] / game_state.max_hp[player]
            start_point[0] += 5
            end_point[0] = bg_pos[0] + start_offset[0] + length * hp_normalized
            end_point[0] -= 5
            thickness = 50
            pygame.draw.line(self.window, pygame.color.Color(140, 100, 0), start_point, end_point, thickness)
            # names
            if player == self.player1_name:
                img = self.player_name_font.render(self.player1_name, True, (0, 0, 0))
                self.window.blit(img, (bg_pos[0] + 110, bg_pos[1] + 14))
            else:
                img = self.player_name_font.render(self.player2_name, True, (0, 0, 0))
                self.window.blit(img, (bg_pos[0] + 110, bg_pos[1] + 14))

    def init_gui_textures(self):
        def load_image(p, name):
            return pygame.image.load(os.path.join(p, name)).convert_alpha()

        path_ = 'assets/images/textures/'

        tank_avatar_offset = (16, 15)
        bullet_offset = (67, 22)

        self.gui_textures[self.player1_name] = [
            (load_image(path_, "gui-background.jpg"), (20, SCR_HEIGHT - 140)),
            (load_image(path_, "tank0avatar.png"), tank_avatar_offset),
            (load_image(path_, "bullet-icon-full.png"), bullet_offset),
            (load_image(path_, "bullet-icon-empty.png"), bullet_offset),
        ]
        self.gui_textures[self.player2_name] = [
            (load_image(path_, "gui-background.jpg"), (SCR_WIDTH-(40 + 280), SCR_HEIGHT - 140)),
            (load_image(path_, "tank1avatar.png"), tank_avatar_offset),
            (load_image(path_, "bullet-icon-full.png"), bullet_offset),
            (load_image(path_, "bullet-icon-empty.png"), bullet_offset),
        ]


def switch_to_menu(ev_manager):
    ev_manager.add_scene_change("single_or_multi_scene")


class FpsRenderSystem:
    def __init__(self, window):
        self.window = window
        self.font_size = 50
        self.font = pygame.font.SysFont(None, self.font_size)
        self.color = (200, 140, 0)
        self.fps_counter_pos = (10, 10)
        self.fps_period = 1  # how often to refresh fps (in seconds)
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