from unittest import TestCase
from world import *


class TestWorld(TestCase):
    def test_when_normalize_scroll(self):
        edge = Vector(5, 7)
        point = Vector(10, 17)
        calc = point.normalized_by(edge)
        expected = Vector(0, 3)
        self.assertEqual(calc, expected)

    def test_when_normalize_negative_scroll(self):
        edge = Vector(5, 7)
        point = Vector(-10, -3)
        calc = point.normalized_by(edge)
        expected = Vector(0, 4)
        self.assertEqual(calc, expected)

    def test_when_put_must_find(self):
        matter = Matter()
        world = World(Vector(7, 5))
        point = Vector(3, 2)
        world.set(point, matter)

        self.assertEqual(matter, world.get(point))

    def test_substitute_when_occupied(self):
        first = Matter()
        world = World(Vector(5, 5))
        world.set(Vector(1, 1), first)

        seccond = Matter()
        world.set(Vector(1, 1), seccond)

        self.assertNotEqual(first, seccond)
