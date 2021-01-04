from functools import singledispatch

from engine.interactions import Resource, InMaking, Actor
from engine.world import World
from engine.vector import Vector, Direction


@singledispatch
def repr(entity, direction: Direction):
    return {
        Direction.FORWARD: '⇡',
        Direction.BACKWARD: '⇣',
        Direction.RIGHT: '⇢',
        Direction.LEFT: '⇠'
    }[direction]


@repr.register
def resource_repr(entity: Resource, direction: Direction):
    return {
        Direction.FORWARD: '△',
        Direction.BACKWARD: '▽',
        Direction.RIGHT: '▷',
        Direction.LEFT: '◁'
    }[direction]


@repr.register
def making_repr(entity: InMaking, direction: Direction):
    return {
        Direction.FORWARD: '▲',
        Direction.BACKWARD: '▼',
        Direction.RIGHT: '▶',
        Direction.LEFT: '◀'
    }[direction]


@repr.register
def actor_repr(entity: Actor, direction: Direction):
    return {
        Direction.FORWARD: '↑',
        Direction.BACKWARD: '↓',
        Direction.RIGHT: '→',
        Direction.LEFT: '←'
    }[direction]


def body_repr(body: World.Body = None):
    return ' ' if body is None else repr(body.entity, body.direction)


class Renderer:

    def __init__(self, world: World):
        self._world = world
        self._world_start = Vector(1, 1)
        self._world_end = world.grid.edge + self._world_start
        self._edge = self._world_end + Vector(2, 1)

    def _blank(self):
        header = '╔' + ('═' * self._world.grid.edge.x) + '╗\n'
        body_r = '║' + (' ' * self._world.grid.edge.x) + '║\n'
        footer = '╚' + ('═' * self._world.grid.edge.x) + '╝\n'
        return header + body_r * self._world.grid.edge.y + footer

    def _index_of(self, position):
        return self._edge.flatten(self._world_start + (position % self._world.grid.edge))

    def render(self):
        screen = []
        screen[:0] = self._blank()
        for body in self._world:
            screen[self._index_of(body.position)] = repr(body.entity, body.direction)
        print(''.join(screen))
