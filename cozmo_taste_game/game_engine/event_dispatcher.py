from typing import Mapping, Callable, Type

from cozmo.event import Event


class EventDispatcher:
    """
    A class to hadle the dispatching of events for the game loop
    """

    def __init__(self) -> None:
        """
        Creates a new instance of the event dispatcher
        """
        self.handlers = dict()

    def add_event_hander(self, event: Type[Event], callback: Callable[..., None]) -> None:
        """
        Adds a handler to the dispatch dictionary
        :param event: the event to listen for
        :param callback: the function to be invoked when the event occurs
        """
        if event.event_name in self.handlers:
            self.handlers[event.event_name].append(callback)
        else:
            self.handlers[event.event_name] = [callback]

    def remove_event_handler(self, event: Type[Event], callback: Callable[..., None]) -> None:
        if event.event_name in self.handlers:
            self.handlers[event.event_name] = [a for a in self.handlers[event.event_name] if a != callback]

    async def notify(self, event: Type[Event], **kw) -> None:
        """
        notifies the registered handler that the event has occurred
        :param event: the event that triggered the notification
        :param kw: any keyword params that should be applied to the event
        :return:
        """
        if event.event_name in self.handlers:
            event = event(**kw)
            for handler in self.handlers[event.event_name]:
                await handler(event)
