from SinglePlayer.src.EntityComponentSystem.Components.Components import Component


class HealthComponent(Component):
    def __init__(self, curr_hp=1000, max_hp=1000):
        self.curr_hp = curr_hp
        self.max_hp = max_hp
        self.last_time_hit = 0
        self.name = __name__.split('.')[-1]
