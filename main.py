from engine.vector import Vector, Direction
from engine.physics import Momentum
from engine.renderer import Renderer
from engine.world import World, Matter


if __name__ == "__main__":
    world = World(Vector(10, 8))
    renderer = Renderer(world)
    world.put_or_raise(Vector(4, 2), Matter())
    world.put_or_raise(Vector(4, 1), Matter())
    world.put_or_raise(Vector(4, 0), Matter())
    for row in range(1000):
        Momentum(Direction.DOWN, 5).push(Vector(4, row % 8), world)




