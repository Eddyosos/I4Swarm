from typing import Optional, List

from engine.maths import Vector


class Matter:
    pass


class Observer:
    def point_changed(self, point: Vector, matter: Optional[Matter]):
        pass

class World:
    def __init__(self, edge: Vector):
        self.edge = edge
        self.__grid__: List[Optional[Matter]] = [None] * edge.x * edge.y
        self.observers: List[Observer] = []

    def subscribe(self, observer: Observer):
        self.observers.append(observer)

    def unsubscribe(self, observer: Observer):
        self.observers.remove(observer)

    def set(self, point: Vector, matter: Matter = None):
        self.__grid__[point.flat_index_by_edge(self.edge)] = matter
        for observer in self.observers:
            observer.point_changed(point % self.edge, matter)

    def get(self, point: Vector):
        return self.__grid__[point.flat_index_by_edge(self.edge)]

    def rows(self):
        for y in range(self.edge.y):
            offset = y * self.edge.x
            yield self.__grid__[offset: offset + self.edge.x]

    def scan(self):
        for index, cell in enumerate(self.__grid__):
            if cell is not None:
                yield cell, self.edge.flat_index_to_point(index)
