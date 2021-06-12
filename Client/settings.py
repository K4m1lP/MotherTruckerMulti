import pygame


AVG_BULLET_DMG = 150

SCR_WIDTH = 1400
SCR_HEIGHT = 900

DEFAULT_EXPLOSION_SIZE = 100

DATABASE = True

GAME_KEYS = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE,
             pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
             pygame.K_KP0, pygame.K_KP1, pygame.K_f, pygame.K_ESCAPE,
             pygame.K_TAB, pygame.K_e]


"""
MAIN CHANGES:
- settings
- systems: game state system
- single game scene
- some parameters in health component / shoot component

"""