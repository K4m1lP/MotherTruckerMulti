class Collision:
    def __init__(self, ent1, ent2, pen_length, pen_vec):
        self.pen_length = pen_length
        self.pen_vec = pen_vec
        self.ent1 = ent1
        self.ent2 = ent2


class CollisionManager:
    __instance = None

    @staticmethod
    def get_instance():
        if not CollisionManager.__instance:
            CollisionManager()
        return CollisionManager.__instance

    def __init__(self):
        if CollisionManager.__instance:
            raise Exception("Class is a singleton!")
        else:
            CollisionManager.__instance = self

            self._collisions_q = []

    def add_collision(self, col):
        self._collisions_q.append(col)

    def get_collisions(self):
        res = self._collisions_q
        self._collisions_q = []
        return res
