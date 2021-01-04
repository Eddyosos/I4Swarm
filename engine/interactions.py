from abc import abstractmethod
from enum import Enum
from functools import partialmethod
from typing import NamedTuple, Any, Iterable, TypeVar, Callable

from engine.vector import Vector, Direction, GridView
from engine.world import World


class Resource:
    pass


class Building:
    pass


T = TypeVar('T')


class InMaking:
    def __init__(self, transform_factory: Callable[[], Any]):
        self._transform_factory = transform_factory
        self._work_done = 0

    def receive_work(self):
        self._work_done += 1

    def is_completed(self):
        return self._work_done > 3

    def transform(self):
        return self._transform_factory() if self.is_completed() else self


class View(NamedTuple):
    entity: Any
    position: Vector
    direction: Direction


class Action(Enum):
    @staticmethod
    def _move(body: World.Body):
        def _push(position: Vector, direction: Direction, strength: int):
            push_body = body.world.grid[position]
            if strength < 1 or push_body is None:
                return
            destiny = direction.translate_vector(position)
            _push(destiny, direction, strength - 1)
            if body.world.grid[destiny] is None:
                push_body.position = destiny

        _push(body.position, body.direction, 3)

    @staticmethod
    def _turn(direction: Direction, body: World.Body):
        body.direction = body.direction.relativize(direction)

    @staticmethod
    def _start_replica(body: World.Body):
        in_front = body.in_front()
        if in_front is not None and isinstance(in_front.entity, Resource):
            in_front.entity = InMaking(body.entity.replicate)

    @staticmethod
    def _start_building(body: World.Body):
        in_front = body.in_front()
        if in_front is not None and isinstance(in_front.entity, Resource):
            in_front.entity = InMaking(Building)

    @staticmethod
    def _work(body: World.Body):
        in_front = body.in_front()
        if in_front is not None and isinstance(in_front.entity, InMaking):
            in_front.entity.receive_work()
            in_front.entity = in_front.entity.transform()

    MOVE = _move
    TURN_RIGHT = partialmethod(_turn, Direction.RIGHT)
    TURN_LEFT = partialmethod(_turn, Direction.LEFT)

    START_REPLICA = _start_replica
    START_BUILDING = _start_building
    WORK = _work

    def __call__(self, *args, **kwargs):
        self.value(*args, **kwargs)


class Actor:
    @abstractmethod
    def act(self, sight: Iterable[View]) -> Action:
        pass

    @classmethod
    def replicate(cls) -> 'Actor':
        return cls()


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

    def tick(self) -> None:
        for body in self.world:
            if isinstance(body.entity, Actor):
                body.entity.act(Perspective(body).view())(body)
