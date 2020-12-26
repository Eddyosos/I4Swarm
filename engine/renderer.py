from typing import Optional

from engine.world import World, Cell
from engine.vector import Vector, Direction


def __cell_repr__(cell: Optional[Cell]):
    return ' ' if cell is None else {
        Direction.UP: '↑',
        Direction.DOWN: '↓',
        Direction.RIGHT: '→',
        Direction.LEFT: '←'
    }[cell.direction]


class Renderer:
    def __init__(self, world: World):
        self.__world__ = world
        self.__world_start__ = Vector(1, 1)
        self.__world_end__ = world.edge + self.__world_start__
        self.__edge__ = self.__world_end__ + Vector(2, 1)

    def __blank__(self):
        header = '╔' + ('═' * self.__world__.edge.x) + '╗\n'
        body_r = '║' + (' ' * self.__world__.edge.x) + '║\n'
        footer = '╚' + ('═' * self.__world__.edge.x) + '╝\n'
        return header + body_r * self.__world__.edge.y + footer

    def __index_of__(self, position):
        return self.__edge__.flatten(self.__world_start__ + (position % self.__world__.edge))

    def render(self):
        screen = []
        screen[:0] = self.__blank__()
        for position, cell in self.__world__.__grid__.items():
            screen[self.__index_of__(position)] = __cell_repr__(cell)
        print(''.join(screen))

