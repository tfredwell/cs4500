class EventDispatcher:

    def __init__(self):
        self.handlers = dict()

    def add_event_hander(self, event, callback):
        if event.event_name in self.handlers:
            self.handlers[event.event_name].append(callback)
        else:
            self.handlers[event.event_name] = [callback]

    async def notify(self, event, **kw):
        if event.event_name in self.handlers:
            event = event(**kw)
            for handler in self.handlers[event.event_name]:
                await handler(event)
