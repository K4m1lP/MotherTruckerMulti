from SinglePlayer.src.EntityComponentSystem.Components.Components import Component


class ShootingComponent(Component):
    def __init__(self, reload_time=0.5, bullet_speed=700, reload_mine_time=1):
        self.reload_time = reload_time  # in seconds
        self.reload_mine_time = reload_mine_time
        self.bullet_speed = bullet_speed  # initial bullet speed
        self.last_time_shot = 0
        self.last_time_mine = 0
        self.name = __name__.split('.')[-1]
