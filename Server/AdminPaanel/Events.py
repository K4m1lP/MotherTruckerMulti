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
        self.scene_events = []
        self.winner = None
        self.exit_event = False

    def add_scene_change(self, scene):
        self.scene_events.append(scene)

    def get_scene_change(self):
        if len(self.scene_events) > 0:
            return self.scene_events.pop()
        return None

    def set_winner(self, winner):
        self.winner = winner

    def get_winner(self):
        res = self.winner
        self.winner = None
        return res
