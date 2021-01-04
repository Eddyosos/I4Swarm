from typing import List

from engine.interactions import Actor, View, Action, Interactor
from engine.renderer import Renderer
from engine.vector import Vector, Direction
from engine.world import World


class Rotator(Actor):

    def replicate(self) -> 'Rotator':
        return Rotator()

    def __init__(self):
        self.last_was_rotate = True

    def act(self, sight: List[View]) -> Action:
        action = Action.MOVE if self.last_was_rotate else Action.TURN_RIGHT
        self.last_was_rotate = not self.last_was_rotate
        return action

# if __name__ == "__main__":
#     world = World(Vector(12, 12))
#     world.insert(Rotator(), Vector(4, 4), Direction.BACKWARD)
#     world.insert(Rotator(), Vector(4, 8), Direction.BACKWARD)
#     world.insert(Rotator(), Vector(8, 4), Direction.BACKWARD)
#     world.insert(Rotator(), Vector(8, 8), Direction.BACKWARD)
#     renderer = Renderer(world)
#     interactor = Interactor(world)
#     for row in range(1000):
#         interactor.tick()
#         renderer.render()
