
import pygame_menu


from Events import Events
from Network import Client

from settings import SCR_HEIGHT, SCR_WIDTH


class Scene:
    def __init__(self, window):
        self.window = window
        self.client = Client.get_instance()
        self.events = Events.get_instance()





