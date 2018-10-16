from direction import Direction


class Ant:
    def __init__(self, colony_pos=(0, 0), direction=Direction.DOWN):
        self.colony_pos = colony_pos
        self.pos = colony_pos
        self.direction = direction
        self.motion = None