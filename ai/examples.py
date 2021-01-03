from typing import List

from engine.interactions import Actor, View, Action


class Rotator(Actor):
    def __init__(self):
        self.last_was_rotate = True

    def act(self, sight: List[View]) -> Action:
        action = Action.MOVE if self.last_was_rotate else Action.TURN_RIGHT
        self.last_was_rotate = not self.last_was_rotate
        return action
