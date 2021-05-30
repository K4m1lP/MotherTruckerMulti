import pygame


class KeyListener:
    __instance = None

    @staticmethod
    def get_instance():
        if not KeyListener.__instance:
            KeyListener()
        return KeyListener.__instance

    def __init__(self):
        if KeyListener.__instance:
            raise Exception("Class is a singleton!")
        else:
            KeyListener.__instance = self
            self.game_keys = [pygame.K_w, pygame.K_d, pygame.K_a, pygame.K_s, pygame.K_SPACE,
                              pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
                              pygame.K_KP0, pygame.K_KP1, pygame.K_f]

            self.pressed_keys = {}
            for key in self.game_keys:
                self.pressed_keys[key] = False

    def is_pressed(self, key):
        return self.pressed_keys.get(key)

    def listen(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key = event.key
                if key in self.game_keys:
                    self.pressed_keys[key] = True
            elif event.type == pygame.KEYUP:
                key = event.key
                if key in self.game_keys:
                    self.pressed_keys[key] = False
            elif event.type == pygame.QUIT:
                return True
        return False

