from enum import Enum


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def succ(self):
        v = self.value + 1
        if v > 3:
            return Direction(0)
        return Direction(v)

    def pred(self):
        v = self.value - 1
        if v < 0:
            return Direction(3)
        return Direction(v)

    @classmethod
    def to_list(cls):
        if not hasattr(cls, 'directions'):
            cls.directions = list(Direction)
        return cls.directions