from dataclasses import dataclass
from typing import Dict
from engine.vector import Vector, Direction


class Entity:
    pass


@dataclass
class Cell:
    entity: Entity
    direction: Direction


class World:
    def __init__(self, edge: Vector):
        self.edge = edge
        self.__grid__: Dict[Vector, Cell] = {}

    def __getitem__(self, position: Vector):
        return self.__grid__.get(position % self.edge)

    def __setitem__(self, position: Vector, cell: Cell):
        self.__grid__[position % self.edge] = cell

    def __delitem__(self, position: Vector):
        del self.__grid__[position % self.edge]

    def push(self, position: Vector, direction: Direction, strength: int):
        if strength < 1 or self[position] is None:
            return
        destiny = position + direction
        self.push(destiny, direction, strength - 1)
        if self[destiny] is None:
            self[destiny] = self[position]
            del self[position]

    def rotate(self, position: Vector, clockwise: bool):
        cell = self[position]
        cell.direction = cell.direction.rotate(clockwise)
