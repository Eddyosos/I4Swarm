from typing import Dict, Any

from engine.vector import Direction, Vector, GridFixed


class World:
    class Body:
        def __init__(self, entity: Any, position: Vector, direction: Direction, world: 'World'):
            self.entity = entity
            self.direction = direction
            self.world = world
            self.world.bodies[id(self)] = self
            self._position = None
            self.position = position

        @property
        def position(self):
            return self._position

        @position.setter
        def position(self, position: Vector):
            self.world.grid[position] = self
            if self.position is not None:
                del self.world.grid[self.position]
            self._position = self.world.grid.simplify(position)

        def in_front(self):
            in_front_position = self.direction.translate_vector(self.position)
            return self.world.grid[in_front_position]

    def __init__(self, edge: Vector):
        self._grid: GridFixed[World.Body] = GridFixed(edge)
        self._bodies: Dict[int, World.Body] = {}

    @property
    def grid(self):
        return self._grid

    @property
    def bodies(self):
        return self._bodies

    def __iter__(self):
        return iter(self.bodies.values())

    def insert(self, entity: Any, position: Vector, direction: Direction):
        World.Body(entity, position, direction, self)
