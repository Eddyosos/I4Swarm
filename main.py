from engine.vector import Vector, Direction
from engine.renderer import Renderer
from engine.world import World, Cell, Entity

if __name__ == "__main__":
    world = World(Vector(10, 8))
    renderer = Renderer(world)
    world[Vector(4, 2)] = Cell(Entity(), Direction.DOWN)
    world[Vector(4, 1)] = Cell(Entity(), Direction.DOWN)
    world[Vector(4, 0)] = Cell(Entity(), Direction.DOWN)
    for row in range(1000):
        world.push(Vector(4, row % 8), Direction.DOWN, 5)
        renderer.render()




