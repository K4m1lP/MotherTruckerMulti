from SinglePlayer.src.EntityComponentSystem.Components.Components import Component


class ControlComponent(Component):
    def __init__(self, id=None, player_name='tmp'):
        self.id = id
        self.player_name = player_name
        self.rotation_speed = 2.5
        self.engine_acc_forward = 20000
        self.engine_acc_backward = 10000
        self.name = __name__.split('.')[-1]
