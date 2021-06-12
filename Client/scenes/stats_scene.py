import pygame_menu

from scenes.scene import Scene
from settings import SCR_HEIGHT, SCR_WIDTH


class StatsScene(Scene):

    def __init__(self, window):
        super().__init__(window)
        self.menu = create_stats_view(self.event_manager, self.client)

    def draw(self, events):
        if self.menu.is_enabled():
            self.menu.update(events)
            self.menu.draw(self.window)

def create_stats_view(events, client):
    stats = client.get_stats()
    menu = pygame_menu.Menu('Mother Trucker', SCR_WIDTH, SCR_HEIGHT, theme=pygame_menu.themes.THEME_DARK)
    text = [
        "Nick: ",
        "Accuracy: ",
        "Shots per battle: ",
        "Wins: ",
        "Number of all battles: ",
        "Moderate damage: "
    ]
    i = 0
    for key in stats:
        if i == 0:
            val = str(str(text[i])+str(stats[key]))
        if i != 0:
            val = str(str(text[i])+str(round(stats[key], 2)))
        i += 1
        menu.add.button(val)

    menu.add.button("Back", back_fun, events)
    return menu

def back_fun(events):
    events.add_scene_change("menu")