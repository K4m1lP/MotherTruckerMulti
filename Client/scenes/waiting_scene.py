from Scenes.scene import Scene


class WaitingScene(Scene):
    def __init__(self, window):
        super().__init__(window)

    def draw(self, events):
        self.window.fill((40, 41, 35))
        # gif = pygame.image.load("../../assets/waiting.gif").convert_alpha()
        # self.window.blit(gif, (SCR_WIDTH / 2 - (gif.get_width() / 2), SCR_HEIGHT / 2 - (gif.get_height() / 2)))
        second_player = self.client.is_second_connected()
        if second_player:
            self.event_manager.add_scene_change("game")

