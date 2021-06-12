import pygame_menu


from event_manager import EventManager
from network import Client

from settings import SCR_HEIGHT, SCR_WIDTH


class Scene:
    def __init__(self, window):
        self.window = window
        self.client = Client.get_instance()
        self.event_manager = EventManager.get_instance()





