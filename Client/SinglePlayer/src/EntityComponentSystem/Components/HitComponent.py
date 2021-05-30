from time import time_ns as get_time

from SinglePlayer.src.EntityComponentSystem.Components.Components import Component


class HitComponent(Component):
    def __init__(self, dmg=100, owner_id=None, activ_time=0):
        self.time_placed = get_time()
        self.activation_time = activ_time
        self.dmg = dmg
        self.owner_id = owner_id
        self.name = __name__.split('.')[-1]

