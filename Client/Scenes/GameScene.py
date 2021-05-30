import os

import pygame
import pygame_menu
from time import time_ns as get_time

from Scenes.Scene import Scene


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
        self.surface = pygame.Surface((1000, 500), pygame.SRCALPHA)

    def draw(self, events):
        is_changed = self.get_keys(events)
        if is_changed:
            self.client.send_key(self.pressed_keys)

        game_state = self.client.get_game_status()
        if game_state:
            self.obj = game_state.to_render

            if game_state.should_exit:
                self.client.block_socket()
                self.events.add_scene_change("game_over_scene")
                self.events.set_winner(game_state.winner)
                return

        if self.obj:
            self.render_sprites(self.obj)

        if self.does_menu and not self.pressed_keys[pygame.K_TAB]:
            # tmp delete
            # self.window.blit(self.surface, (0, 0))
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
        huj = False
        for code in self.prev_pressed_keys:
            if self.prev_pressed_keys[code] != self.pressed_keys[code]:
                huj = True
            self.prev_pressed_keys[code] = self.pressed_keys[code]
        return huj

    def render_sprites(self, sprites):
        sprites.sort(key=lambda s: s.z)
        if sprites:
            for sprite in sprites:
                x = sprite.pos.x
                y = sprite.pos.y
                # if new, save to ram not to access disc every frame
                image_name = sprite.img_name
                if image_name not in self.images:
                    self.images[image_name] = pygame.image.load(os.path.join('assets/images/textures/', image_name)).convert_alpha()
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


def exit_fun(events):
    events.exit_event = True
