from ws_connection import ClientClosedError
from ws_server import WebSocketServer, WebSocketClient

class Client(WebSocketClient):
    def __init__(self, conn):
        super().__init__(conn)

    def process(self):
        try:
            msg = self.connection.read()
            if not msg:
                return
            msg = msg.decode("utf-8")
            print(str(msg))
        except ClientClosedError:
            print("ERROR")
            self.connection.close()


class Server(WebSocketServer):
    def __init__(self):
        super().__init__("index.html", 2)

    def _make_client(self, conn):
        return Client(conn)


server = Server()
server.start()
try:
    while True:
        server.process_all()
except KeyboardInterrupt:
    pass
server.stop()