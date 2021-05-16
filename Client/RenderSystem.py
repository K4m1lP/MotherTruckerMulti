import pygame

SCR_WIDTH, SCR_HEIGHT = 1900, 1000
RED = 255, 0, 0
YELLOW = 255, 255, 0


class RenderSystem:
    def __init__(self, window):
        self.window = window
        self.fps_sys = FpsRenderSystem(window)

    def render(self, pos_comp, rend_comp, hb_comp):
        x = pos_comp.pos.x
        y = pos_comp.pos.y

        # don't show objects that are outside camera view
        if not (-100 <= x <= SCR_WIDTH + 100 and -100 <= y <= SCR_HEIGHT + 100):
            return
        image = rend_comp.img
        size = rend_comp.size
        angle = pos_comp.orient.get_angle()

        # scale and rotate image
        image = pygame.transform.rotate(pygame.transform.scale(image, size), angle)

        render_pos = (int(x - image.get_width() / 2), int(y - image.get_height() / 2))
        self.window.blit(image, render_pos)

    def update(self, dt, data):
        '''
        data = [{"PositionComponent": {Object}}, {}, ...]
        :param dt:
        :param data:
        :return:
        '''
        if data:
            for entity in data:
                pos_comp = entity["PositionComponent"]
                rend_comp = entity["RenderComponent"]
                hb_comp = entity["HitboxComponent"]
                if pos_comp and rend_comp:
                    self.render(pos_comp, rend_comp, hb_comp)
            self.fps_sys.update(dt)


class FpsRenderSystem:
    def __init__(self, window):
        self.window = window
        self.font_size = 50
        self.font = pygame.font.SysFont(None, self.font_size)
        self.color = (0, 0, 0)  # black
        self.fps_counter_pos = (40, 40)
        self.fps_period = 1  # how often to refresh fps
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

