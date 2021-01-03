from ai.examples import Rotator
from engine.interactions import Interactor
from engine.vector import Vector, Direction
from engine.renderer import Renderer
from engine.world import World

if __name__ == "__main__":
    world = World(Vector(10, 8))
    world.insert(Rotator(), Vector(4, 2), Direction.BACKWARD)
    world.insert(Rotator(), Vector(4, 1), Direction.BACKWARD)
    world.insert(Rotator(), Vector(4, 0), Direction.BACKWARD)
    renderer = Renderer(world)
    interactor = Interactor(world)
    for row in range(1000):
        interactor.tick()
        renderer.render()




