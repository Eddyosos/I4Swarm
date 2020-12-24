from typing import TypeVar, Generic, List

E = TypeVar('E')


class Observer(Generic[E]):
    def notify(self, event: E):
        pass


class Observable(Generic[E]):
    def __init__(self):
        self.observers: List[Observer[E]] = []

    def notify(self, event: E):
        for observer in self.observers:
            observer.notify(event)


class Grid(Observable[])