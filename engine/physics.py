from dataclasses import dataclass

from engine.vector import *
from engine.world import World


@dataclass
class Momentum:
    orientation: Direction
    module: int = 1

    def push(self, point: Vector):
        matter = world.get(point)
        if self.module < 1 or matter is None:
            return matter
        destiny_point = point + self.orientation
        destiny_matter = Momentum(self.orientation, self.module - 1).push(destiny_point, world)
        if destiny_matter is None:
            world.move_or_raise(point, destiny_point)
            return None
        else:
            return matter
