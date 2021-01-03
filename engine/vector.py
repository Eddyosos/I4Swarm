from enum import Enum, auto
from typing import NamedTuple, Generic, List, TypeVar, Optional

from engine import Error


class Vector(NamedTuple):
    x: int
    y: int

    def flat(self) -> int:
        return self.x * self.y

    def flatten(self, other: 'Vector') -> int:
        n = other % self
        return n.x + n.y * self.x

    def vectorize(self, index: int) -> 'Vector':
        return Vector(index % self.x, index // self.x % self.y)

    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x + other.x, self.y + other.y)

    def __mod__(self, other) -> 'Vector':
        return Vector(self.x % other.x, self.y % other.y)

    def __mul__(self, other) -> 'Vector':
        return Vector(self.x * other.x, self.y * other.y)

    def rotate_clockwise(self):
        return Vector(-self.y, self.x)


class MovementAndRotation(NamedTuple):
    movement: Vector = Vector(0, -1)
    rotation: Vector = Vector(1, 1)

    def next(self):
        return MovementAndRotation(self.movement.rotate_clockwise(), self.rotation.rotate_clockwise())


class Direction(MovementAndRotation, Enum):
    def _generate_next_value_(name, start, count, last_values):
        if not last_values:
            return MovementAndRotation()
        else:
            return last_values[-1].next()

    FORWARD = auto()
    RIGHT = auto()
    BACKWARD = auto()
    LEFT = auto()

    @staticmethod
    def __clockwise__():
        return tuple(Direction)

    def __clockwise_index__(self):
        return self.__clockwise__().index(self)

    def __bound__(self, index: int):
        return index % len(self.__clockwise__())

    def relativize(self, other: 'Direction'):
        index = other.__clockwise_index__() + self.__clockwise_index__()
        return self.__clockwise__()[self.__bound__(index)]

    def rotate_vector(self, vector: Vector) -> Vector:
        return self.rotation * vector

    def translate_vector(self, vector: Vector) -> Vector:
        return self.movement + vector


T = TypeVar('T')


class GridFixed(Generic[T]):
    def __init__(self, edge: Vector):
        self._edge = edge
        self._grid: List[Optional[T]] = [None] * edge.flat()

    @property
    def edge(self):
        return self._edge

    def _grid_index(self, position: Vector) -> int:
        return self.edge.flatten(position)

    def __getitem__(self, position: Vector) -> Optional[T]:
        return self._grid[self._grid_index(position)]

    class PositionOccupied(Error):
        pass

    def __setitem__(self, position: Vector, t: T) -> None:
        if self[position] is not None:
            raise GridFixed.PositionOccupied()
        self._grid[self._grid_index(position)] = t

    def __delitem__(self, position: Vector) -> None:
        self._grid[self._grid_index(position)] = None

    def simplify(self, vector: Vector):
        return vector % self.edge


class GridView:

    def __init__(self, grid: GridFixed, position: Vector, direction: Direction):
        self._grid = grid
        self._position = position
        self._direction = direction

    def __getitem__(self, position: Vector) -> Optional[T]:
        return self._grid[self._position + self._direction.rotate_vector(position)]
