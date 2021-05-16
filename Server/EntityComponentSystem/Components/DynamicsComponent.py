from EntityComponentSystem.Components.Components import Component
from EntityComponentSystem.Vec2d import Vec2d


class DynamicsComponent(Component):

    def __init__(self, vel=Vec2d(0, 0), force=Vec2d(0, 0), mass=None):
        self.vel = vel
        self.force = force
        self.inverse_mass = 0
        if mass:
            self.inverse_mass = 1 / mass
        self.name = __name__.split('.')[-1]
