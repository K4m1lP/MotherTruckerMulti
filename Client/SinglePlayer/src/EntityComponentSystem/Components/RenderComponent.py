from SinglePlayer.src.EntityComponentSystem.Components.Components import Component


class RenderComponent(Component):
    def __init__(self, img_name=None, size=None, fixed_orient=False, fixed_size=False):
        self.img_name = img_name
        self.fixed_size = fixed_size
        self.fixed_orient = fixed_orient
        self.size = size
        self.name = __name__.split('.')[-1]
