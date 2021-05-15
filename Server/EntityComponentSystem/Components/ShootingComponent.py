from EntityComponentSystem.Components.Components import Component


class ShootingComponent(Component):
    def __init__(self, reload_time=1.5, bullet_speed=1000):
        self.reload_time = reload_time  # in seconds
        self.bullet_speed = bullet_speed  # initial bullet speed
        self.last_time_shot = 0
        self.name = __name__.split('.')[-1]
