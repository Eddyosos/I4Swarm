from enum import Enum
from typing import NamedTuple


class Vector(NamedTuple):
    x: int
    y: int

    def flat(self):
        return self.x * self.y

    def flatten(self, other: 'Vector'):
        n = other % self
        return n.x + n.y * self.x

    def vectorize(self, index: int):
        return Vector(index % self.x, index // self.x % self.y)

    def __add__(self, other: 'Vector'):
        return Vector(self.x + other.x, self.y + other.y)

    def __mod__(self, other):
        return Vector(self.x % other.x, self.y % other.y)


class Direction(Vector, Enum):
    UP = Vector(0, -1)
    RIGHT = Vector(1, 0)
    DOWN = Vector(0, 1)
    LEFT = Vector(-1, 0)

    def rotate(self, clockwise: bool):
        dirs = list(Direction)
        index = dirs.index(self) + (1 if clockwise else -1)
        return dirs[index % len(dirs)]