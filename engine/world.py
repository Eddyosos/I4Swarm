from dataclasses import dataclass

from typing import Optional, List

from engine.vector import Vector, Direction
from engine.observer import Observable


class Full(Exception):
    pass


class Empty(Exception):
    pass


class Entity:
    pass


@dataclass
class Cell:
    entity: Entity
    direction: Direction

@dataclass
class Body(Cell):
    position: Vector

class Changes:
    pass

class World(Observable[Changes]):

    def __init__(self, edge: Vector):
        super(World, self).__init__()
        self.edge = edge
        self.__grid__: List[Optional[Body]] = [None] * edge.flat()
        self.__entities__:  List[Body] = []

    def __setitem__(self, position: Vector, cell: Cell):
        self.__delitem__(position)

        body = Body(cell.entity, cell.direction, position)
        self.__grid__[self.edge.deflate(position)] = body
        self.__entities__.append(body)

    def __delitem__(self, position: Vector):
        index = self.edge.deflate(position)
        body = self.__grid__[index]
        self.__grid__[index] = None
        if body is not None:
            self.__entities__.remove(body)

    def __getitem__(self, position: Vector) -> Optional[Cell]:
        return self.__grid__[self.edge.deflate(position)]






