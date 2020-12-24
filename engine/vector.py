from dataclasses import dataclass
from enum import Enum


@dataclass
class Vector:
    x: int
    y: int

    def flat(self):
        return self.x * self.y

    def deflate(self, other: 'Vector'):
        n = other % self
        return n.x + n.y * self.x

    def inflate(self, index: int):
        return Vector(index % self.x, index // self.x % self.y)

    def __add__(self, other: 'Vector'):
        return Vector(self.x + other.x, self.y + other.y)

    def __mod__(self, other):
        return Vector(self.x % other.x, self.y % other.y)


class Direction(Vector, Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)
