import os

import pygame

from SinglePlayer.src.EntityComponentSystem.Components.HitboxComponent import HitboxComponent
from SinglePlayer.src.EntityComponentSystem.Components.PositionComponent import PositionComponent
from SinglePlayer.src.EntityComponentSystem.Components.RenderComponent import RenderComponent
from SinglePlayer.src.EntityComponentSystem.System.FpsRenderSystem import FpsRenderSystem
from SinglePlayer.src.EntityComponentSystem.System.System import System
from SinglePlayer.src.settings import SUPER_TURBO_PROGRAMMER_MODE

RED = 255, 0, 0
YELLOW = 255, 255, 0


class RenderSystem(System):
    def __init__(self, entity_manager, window):
        super().__init__(entity_manager)
        self.window = window
        self.fps_sys = FpsRenderSystem(entity_manager, window)
        self.images = {}

    def render(self, pos_comp, rend_comp, hb_comp):
        # if new, save to ram not to access disc every frame
        image_name = rend_comp.img_name
        if image_name not in self.images:
            self.images[image_name] = pygame.image.load(os.path.join('assets/images/textures/', image_name))
            if rend_comp.size and rend_comp.fixed_size:
                self.images[image_name] = pygame.transform.scale(self.images[image_name], rend_comp.size)

        image = self.images[image_name]
        size = rend_comp.size
        angle = pos_comp.orient.get_angle()
        if size and not rend_comp.fixed_size: image = pygame.transform.scale(image, size)
        if not rend_comp.fixed_orient: image = pygame.transform.rotate(image, angle)

        x = pos_comp.pos.x
        y = pos_comp.pos.y
        # render
        if SUPER_TURBO_PROGRAMMER_MODE:
            if hb_comp:
                points = hb_comp.transformed_vertices
                if points[0]:
                    for i in range(len(points)):
                        p1 = points[i].x, points[i].y
                        p2 = points[(i + 1) % len(points)].x, points[(i + 1) % len(points)].y
                        if hb_comp.overlap:
                            pygame.draw.line(self.window, RED, p1, p2)
                        else:
                            pygame.draw.line(self.window, YELLOW, p1, p2)
        else:
            render_pos = (int(x - image.get_width() / 2), int(y - image.get_height() / 2))
            self.window.blit(image, render_pos)

    def update(self, dt):

        self.window.fill((220, 210, 200))

        entities = self.entity_manager.get_entities(RenderComponent())
        for entity in entities:
            pos_comp = self.entity_manager.get_component(PositionComponent(), entity)
            rend_comp = self.entity_manager.get_component(RenderComponent(), entity)
            hb_comp = self.entity_manager.get_component(HitboxComponent(), entity)

            if pos_comp and rend_comp:
                self.render(pos_comp, rend_comp, hb_comp)

        self.fps_sys.update(dt)
