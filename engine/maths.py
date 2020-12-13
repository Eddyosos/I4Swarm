from dataclasses import dataclass
from enum import Enum


@dataclass
class Vector:
    x: int
    y: int

    def flat_index_by_edge(self, edge: 'Vector'):
        n = self % edge
        return n.x + n.y * edge.x

    def flat_index_to_point(self, flat_index: int):
        return Vector(flat_index % self.x, flat_index // self.x % self.y)

    def __add__(self, other: 'Vector'):
        return Vector(self.x + other.x, self.y + other.y)

    def __mod__(self, other):
        return Vector(self.x % other.x, self.y % other.y)


class Unit(Vector, Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)
