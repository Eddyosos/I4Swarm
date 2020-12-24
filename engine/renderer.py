from typing import Optional

from engine.observer import Observer
from engine.world import World, Matter, Change
from engine.vector import Vector


def __cell_repr__(cell: Optional[Matter]):
    return ' ' if cell is None else '#'


class Renderer(Observer[Change]):
    def __init__(self, world: World):
        self.world = world
        self.world_start = Vector(1, 1)
        self.world_end = world.edge + self.world_start
        self.edge = self.world_end + Vector(2, 1)
        self.screen = '╔' + ('═' * self.world.edge.x) + '╗\n' + \
                      ''.join('║' + ''.join(map(__cell_repr__, row)) + '║\n' for row in self.world.rows()) + \
                      '╚' + ('═' * self.world.edge.x) + '╝\n'
        world.observers.append(self)

    def __translate__(self, world_point: Vector):
        return self.world_start + world_point

    def __index_of__(self, world_point: Vector):
        return self.__translate__(world_point).flat_index_by_edge(self.edge)

    def __update__(self, matter, world_point):
        i = self.__index_of__(world_point)
        self.screen = self.screen[:i] + __cell_repr__(matter) + self.screen[i + 1:]

    def notify(self, event: Change):
        pass
    #     handlers?

    def render(self):
        print(self.screen)

    def __repr__(self):
        return self.screen
