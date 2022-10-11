import typing
import functools

SendFunc = typing.Callable[[str, dict], typing.Any]

class WebSocketHandler:
    def __init__(self, _id: str, send_func: SendFunc):
        self.id = _id
        self.send = send_func
        self.reply = functools.partial(self.send, self.id)
    def connect(self):
        print("connect")
        self.reply("test")
    def event(self, data):
        print("event", data)
    def disconnect(self):
        print("disconnect")
