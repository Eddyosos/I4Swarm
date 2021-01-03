from abc import abstractmethod
from enum import Enum
from functools import partialmethod
from typing import NamedTuple, Any, Iterable

from engine.vector import Vector, Direction, GridView
from engine.world import World


class View(NamedTuple):
    entity: Any
    position: Vector
    direction: Direction


class Action(Enum):
    @staticmethod
    def __move__(body: World.Body):
        def __push__(position: Vector, direction: Direction, strength: int):
            push_body = body.world.grid[position]
            if strength < 1 or push_body is None:
                return
            destiny = direction.translate_vector(position)
            __push__(destiny, direction, strength - 1)
            if body.world.grid[destiny] is None:
                push_body.position = destiny

        __push__(body.position, body.direction, 3)

    @staticmethod
    def __turn__(direction: Direction, body: World.Body):
        body.direction = body.direction.relativize(direction)

    MOVE = __move__
    TURN_RIGHT = partialmethod(__turn__, Direction.RIGHT)
    TURN_LEFT = partialmethod(__turn__, Direction.LEFT)

    def __call__(self, *args, **kwargs):
        self.value(*args, **kwargs)


class Actor:
    @abstractmethod
    def act(self, sight: Iterable[View]) -> Action:
        pass


class Perspective:
    def __init__(self, body: World.Body):
        self._body = body
        self._grid = GridView(body.world.grid, body.position, body.direction)

    def __getitem__(self, position: Vector):
        view = self._grid[position]
        if view is not None:
            return View(view.entity, position, self._body.direction.relativize(view.direction))
        else:
            return None

    def view(self) -> Iterable[View]:
        view_pos = (Vector(x, -y) for y in range(5) for x in range(-y, 1 + y))
        views = (self[pos] for pos in view_pos)
        yield from filter(None, views)


class Interactor:

    def __init__(self, world: World):
        self.world = world

    def tick(self):
        for body in self.world:
            if isinstance(body.entity, Actor):
                body.entity.act(Perspective(body).view())(body)
