from EntityComponentSystem.Components.Components import Component


class ControlComponent(Component):
    def __init__(self, player_name='tmp'):
        self.player_name = player_name
        self.rotation_speed = 1.8
        self.engine_acc_forward = 20000
        self.engine_acc_backward = 5000
        self.name = __name__.split('.')[-1]
