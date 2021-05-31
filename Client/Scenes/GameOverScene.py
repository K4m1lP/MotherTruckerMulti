import pygame_menu

from Scenes.Scene import Scene
from settings import SCR_WIDTH, SCR_HEIGHT


class GameOverScene(Scene):
    def __init__(self, window):
        super().__init__(window)
        self.menu = create_game_over_view(self.client, self.events)

    def draw(self, events):
        if self.menu.is_enabled():
            self.menu.update(events)
            self.menu.draw(self.window)


def create_game_over_view(client, events):
    menu = pygame_menu.Menu('Mother Trucker', SCR_WIDTH, SCR_HEIGHT, theme=pygame_menu.themes.THEME_DARK)
    menu.add.label("Game over")
    winner = events.get_winner()
    text = "Winner: " + winner
    menu.add.label(text)
    menu.add.button('Continue', continue_function, client, events)
    return menu


def continue_function(client, events):
    events.add_scene_change("single_or_multi_scene")

