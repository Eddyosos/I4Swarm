from dataclasses import dataclass

from engine.maths import *
from engine.world import World


@dataclass
class Momentum:
    orientation: Unit
    module: int = 1

    def push(self, point: Vector, world: World):
        matter = world.get(point)
        if self.module < 1 or matter is None:
            return matter
        destiny_point = point + self.orientation
        destiny_matter = Momentum(self.orientation, self.module - 1).push(destiny_point, world)
        if destiny_matter is None:
            world.set(point, None)
            world.set(destiny_point, matter)
            return None
        else:
            return matter
