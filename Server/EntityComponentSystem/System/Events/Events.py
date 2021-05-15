class Events:
    __instance = None

    @staticmethod
    def get_instance():
        if not Events.__instance:
            Events()
        return Events.__instance

    def __init__(self):
        if Events.__instance:
            raise Exception("Class is a singleton!")
        else:
            Events.__instance = self
            self.events_dict = {
                "shoot": [],
                "click": [],
                "arrow_menu": [],
                "scene": []
            }

    def add_click(self, pos):
        self.events_dict["click"].append(pos)

    def get_click(self):
        if self.events_dict["click"]:
            return self.events_dict["click"].pop()

    def clear_click(self):
        self.events_dict["click"] = []

    def add_arrow(self, pos):
        self.events_dict["arrow_menu"].append(pos)

    def get_arrow(self):
        if self.events_dict["arrow_menu"]:
            return self.events_dict["arrow_menu"].pop()

    def clear_arrow(self):
        self.events_dict["arrow_menu"] = []

    def add_shoot(self, obj):
        self.events_dict["shoot"].append(obj)

    def clear(self):
        for i in self.events_dict.keys():
            self.events_dict[i] = []

    def add_scene(self, pos):
        self.events_dict["scene"].append(pos)

    def get_scene(self):
        if self.events_dict["scene"]:
            return self.events_dict["scene"].pop()

    def clear_scene(self):
        self.events_dict["scene"] = []
