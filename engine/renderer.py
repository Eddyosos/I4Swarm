from engine.world import World
from engine.vector import Vector, Direction


class Renderer:
    @staticmethod
    def __body_repr__(body: World.Body = None):
        return ' ' if body is None else {
            Direction.FORWARD: '↑',
            Direction.BACKWARD: '↓',
            Direction.RIGHT: '→',
            Direction.LEFT: '←'
        }[body.direction]

    def __init__(self, world: World):
        self._world = world
        self._world_start = Vector(1, 1)
        self._world_end = world.grid.edge + self._world_start
        self._edge = self._world_end + Vector(2, 1)

    def __blank__(self):
        header = '╔' + ('═' * self._world.grid.edge.x) + '╗\n'
        body_r = '║' + (' ' * self._world.grid.edge.x) + '║\n'
        footer = '╚' + ('═' * self._world.grid.edge.x) + '╝\n'
        return header + body_r * self._world.grid.edge.y + footer

    def __index_of__(self, position):
        return self._edge.flatten(self._world_start + (position % self._world.grid.edge))

    def render(self):
        screen = []
        screen[:0] = self.__blank__()
        for body in self._world:
            screen[self.__index_of__(body.position)] = self.__body_repr__(body)
        print(''.join(screen))

