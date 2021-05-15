import pygame
import os

from EntityComponentSystem.Components.Components import Component


class RenderComponent(Component):
    def __init__(self, img=None, size=(10, 10), ready=False):
        self.img = None
        if img and not ready:
            self.img = pygame.image.load(os.path.join('../../assets/images/textures/', img))
        elif img and ready:
            self.img = img
        else:
            self.img = pygame.image.load(os.path.join('../../assets/images/textures/', 'DEFAULT_TEXTURE.png'))
        self.size = size
        self.name = __name__.split('.')[-1]
