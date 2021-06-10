
import pygame_menu

import DBManager
import MockDB
from AdminPaanel.Events import Events
from settings import DATA_BASE


class Scene:
    def __init__(self, window):
        self.window = window
        self.client = None
        if DATA_BASE:
            self.client = DBManager
        else:
            self.client = MockDB
        self.events = Events.get_instance()





