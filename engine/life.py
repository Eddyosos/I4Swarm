from dataclasses import dataclass
from typing import Dict

from engine.maths import Vector, Unit
from engine.world import World, Matter, Observer


class Being(Matter):
    pass


@dataclass
class Pose:
    position: Vector
    orientation: Unit


class Life(Observer):
    def __init__(self, world: World):
        self.world = world
        # self.beings: Dict[Being, Pose] = {k: Pose(pos, )}
        world.subscribe(self)
