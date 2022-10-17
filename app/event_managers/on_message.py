class OnMessageEventManager():
    _event_handlers = []

    def __init__(self):
        self._event_handlers = []

    def add(self, handler):
        self._event_handlers.append(handler)

    async def call_handlers(self, *args, **keywargs):
        for handler in self._event_handlers:
            await handler(*args, **keywargs)


on_message_event_handler = OnMessageEventManager()


def on_message_subscriber(command_string, is_dm=False):
    def decorator(event_handler):
        async def event_handler_checker(message):
            command_format = f'!{command_string}'

            if message.content.startswith(command_format):
                if is_dm:
                    if not message.guild:
                        await event_handler(message)
                else:
                    await event_handler(message)

        on_message_event_handler.add(event_handler_checker)

        def wrapper():
            event_handler()

        return wrapper

    return decorator
