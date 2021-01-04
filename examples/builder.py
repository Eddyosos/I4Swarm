from typing import List

from engine.interactions import Actor, View, Action, Interactor, Resource
from engine.renderer import Renderer
from engine.vector import Vector, Direction
from engine.world import World


class Builder(Actor):

    def __init__(self):
        self.has_started = False

    def replicate(self) -> 'Builder':
        return Builder()

    def act(self, sight: List[View]) -> Action:
        action = Action.WORK if self.has_started else Action.START_REPLICA
        self.has_started = True
        return action


if __name__ == "__main__":
    world = World(Vector(12, 12))
    position = Vector(4, 4)
    world.insert(Builder(), position, Direction.BACKWARD)
    position = Direction.BACKWARD.translate_vector(position)
    world.insert(Resource(), position, Direction.BACKWARD)
    position = Direction.BACKWARD.translate_vector(position)
    world.insert(Resource(), position, Direction.BACKWARD)

    renderer = Renderer(world)
    interactor = Interactor(world)
    renderer.render()
    for _ in range(12):
        interactor.tick()
        renderer.render()
