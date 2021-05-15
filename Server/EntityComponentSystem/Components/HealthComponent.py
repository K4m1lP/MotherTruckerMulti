from EntityComponentSystem.Components.Components import Component


class HealthComponent(Component):
    def __init__(self, cur_hp=0, max_hp=100):
        self.cur_hp = cur_hp
        self.max_hp = max_hp
        self.alive = True
        self.name = __name__.split('.')[-1]
