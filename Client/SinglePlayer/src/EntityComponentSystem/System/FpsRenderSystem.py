import pygame

from SinglePlayer.src.EntityComponentSystem.System.System import System


class FpsRenderSystem(System):
    def __init__(self, entity_manager, window):
        super().__init__(entity_manager)
        self.window = window
        self.font_size = 50
        self.font = pygame.font.SysFont(None, self.font_size)
        self.color = (255, 0, 0)  # red
        self.fps_counter_pos = (55, 55)
        self.fps_period = 0.7  # how often to refresh fps
        self.fps_time_left = 0
        self.fps_tmp_curr_val = 0

    def update(self, dt):
        if self.fps_time_left <= 0:
            self.fps_tmp_curr_val = int(round(1 / dt, 0))
            self.fps_time_left = self.fps_period
        else:
            self.fps_time_left -= dt
        img = self.font.render(repr(self.fps_tmp_curr_val), True, self.color)
        self.window.blit(img, self.fps_counter_pos)
