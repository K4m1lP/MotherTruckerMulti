from SinglePlayer.src.EntityComponentSystem.Components.Components import Component
from SinglePlayer.src.utils.Vec2d import Vec2d


class HitboxComponent(Component):
    def __init__(self, size=(0, 0)):
        self.name = __name__.split('.')[-1]
        self.vertices = [Vec2d(size[0] / (-2), size[1] / (-2)),  # bottom left
                         Vec2d(size[0] / 2, size[1] / (-2)),  # bottom right
                         Vec2d(size[0] / 2, size[1] / 2),  # top right
                         Vec2d(size[0] / (-2), size[1] / 2)]  # top left
        self.transformed_vertices = [None] * len(self.vertices)
        self.overlap = False
        self.is_dirty = True
        self.r_squared = (size[0] / 2) ** 2 + (size[1] / 2) ** 2
