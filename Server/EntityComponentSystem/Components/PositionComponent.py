from EntityComponentSystem.Components.Components import Component
from utils.Vec2d import Vec2d


class PositionComponent(Component):
    def __init__(self, pos=Vec2d(0, 0), orient=Vec2d(1, 0), z=0):
        self.orient = orient
        self.pos = pos
        self.z = z
        self.name = __name__.split('.')[-1]
