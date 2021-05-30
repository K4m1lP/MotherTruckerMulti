from SinglePlayer.src.EntityComponentSystem.Components.Components import Component


class AnimationComponent(Component):
    def __init__(self, img_num=1, img_name='explosion'):
        self.img_name = img_name
        self.img_num = img_num
        self.curr_img_idx = -1
        self.entire_time = 0.5 * 1e9
        self.change_time = self.entire_time / self.img_num
        self.last_time_changed = 0
        self.name = __name__.split('.')[-1]

