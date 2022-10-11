import flask
import flask_socketio
import pathlib

import ws as ws_mod

class App:
    def __init__(self):
        self._project_dir = pathlib.Path(__file__).parent
        self._static_dir = self._project_dir / "static"

        self.app = flask.Flask(__name__)
        self.app.config["SECRET_KEY"] = "secret!"
        self.socketio = flask_socketio.SocketIO(self.app)

        self.socketio.on("connect")(self._on_connect)
        self.socketio.on("event")(self._on_event)
        self.socketio.on("disconnect")(self._on_disconnect)

        self.app.route("/")(self._render)
        self.app.route("/<string:file_name>")(self._resource)

        self.rooms = {}
        self.sockets: dict[str, ws_mod.WebSocketHandler] = {}
        self._send_func: ws_mod.SendFunc = lambda to, data: self.socketio.emit("event", data, to = to)
    def _render(self):
        return flask.send_file(self._static_dir / "hub.html")
    def _resource(self, file_name: str):
        return flask.send_from_directory(self._static_dir, file_name)
    def _on_connect(self):
        _id = flask.request.sid

        ws = ws_mod.WebSocketHandler(_id, self._send_func)
        self.sockets[_id] = ws
        ws.connect()
    def _on_event(self, data):
        _id = flask.request.sid

        self.sockets[_id].event(data)
    def _on_disconnect(self):
        _id = flask.request.sid

        self.sockets[_id].disconnect()
        del self.sockets[_id]
    def run(self):
        self.socketio.run(self.app)

if __name__ == "__main__":
    app = App()
    app.run()
