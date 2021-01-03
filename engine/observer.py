from typing import TypeVar, Generic, NamedTuple, Dict, Callable, Type

Owner = TypeVar('Owner')
Attribute = TypeVar('Attribute')


class Change(Generic[Owner, Attribute], NamedTuple):
    obj: Owner
    attr_name: str
    old: Attribute
    new: Attribute


Subscriber = Callable[[Change[Owner, Attribute]], None]


class Publisher(Generic[Owner, Attribute]):

    def __set_name__(self, owner: Type[Owner], name: str) -> None:
        self.name = name
        self.on_change_call_name = '_' + name + '_on_change_call'
        self.subscribe_change_name = name + '_subscribe_change'
        setattr(owner, self.subscribe_change_name, self.subscribe_change)

    def _on_change_call(self, instance: object) -> Dict[int, Subscriber]:
        try:
            return getattr(instance, self.on_change_call_name)
        except AttributeError:
            default = {}
            setattr(instance, self.on_change_call_name, default)
            return default

    def subscribe_change(self, instance: Owner, on_change: Subscriber) -> None:
        self._on_change_call(instance)[id(on_change)] = on_change

    def notify_change(self, change: Change[Owner, Attribute]) -> None:
        for subscriber_call in self._on_change_call(change.obj).values():
            subscriber_call(change)

    def __get__(self, instance: Owner, owner: Type[Owner]) -> Attribute:
        return getattr(instance, self.name)

    def __set__(self, instance: Owner, value: Attribute) -> None:
        old = getattr(instance, self.name)
        setattr(instance, self.name, value)
        self._on_change_call(Change(instance, self.name, old, value))

    def __delete__(self, instance: Owner) -> None:
        delattr(instance, self.on_change_call_name)
        delattr(instance, self.subscribe_change_name)
