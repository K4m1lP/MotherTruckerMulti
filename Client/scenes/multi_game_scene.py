import os

import pygame
import pygame_menu
from time import time_ns as get_time

from scenes.scene import Scene


class MultiGameScene(Scene):
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
        self.menu.add.button("Quit", exit_fun, self.event_manager)
        self.score_tab = pygame_menu.Menu(title="Score tab", height=250, width=500, theme=pygame_menu.themes.THEME_DARK)
        self.score_tab.add.label("Your hp: ")
        self.score_tab.add.label("Opponent hp: ")
        self.surface = pygame.Surface((1000, 500), pygame.SRCALPHA)
        self.fps_sys = FpsRenderSystem(window)
        self.end_time = None
        self.end_time_frame_ended = get_time()

    def draw(self, events):
        dt = (get_time() - self.end_time_frame_ended) * 1e-9
        self.end_time_frame_ended = get_time()
        is_changed = self.get_keys(events)
        if is_changed:
            self.client.send_key(self.pressed_keys)

        game_state = self.client.get_game_state()
        if game_state:
            self.obj = game_state.to_render

            if game_state.should_exit:
                self.client.block_socket()
                self.event_manager.add_scene_change("game_over_scene")
                self.event_manager.set_winner(game_state.looser)
                return

        if self.obj:
            self.render_all(self.obj, dt)

        if self.does_menu and not self.pressed_keys[pygame.K_TAB]:
            if self.menu.is_enabled():
                self.menu.update(events)
                self.menu.draw(self.window)

        if self.pressed_keys[pygame.K_TAB] and not self.does_menu:
            self.window.blit(self.surface, (0, 0))
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
        is_changed = False
        for code in self.prev_pressed_keys:
            if self.prev_pressed_keys[code] != self.pressed_keys[code]:
                is_changed = True
            self.prev_pressed_keys[code] = self.pressed_keys[code]
        return is_changed

    def render_all(self, sprites, dt):
        sprites.sort(key=lambda s: s.z)
        if sprites:
            for sprite in sprites:
                x = sprite.pos.x
                y = sprite.pos.y
                # if new, save to ram not to access disc every frame
                image_name = sprite.img_name
                if image_name not in self.images:
                    self.images[image_name] = pygame.image.load(
                        os.path.join('assets/images/textures/', image_name)).convert_alpha()
                    if sprite.size and sprite.fixed_size:
                        self.images[image_name] = pygame.transform.scale(self.images[image_name], sprite.size)
                elif image_name == 'tile.png':
                    self.images[image_name] = pygame.image.load(
                        os.path.join('assets/images/textures/', image_name)).convert_alpha()
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
