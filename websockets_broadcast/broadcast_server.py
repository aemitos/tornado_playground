# -*- coding: utf-8 -*-
# Application that receives text messages from POST requests and
# broadcast them to all open websockets

import tornado.ioloop
import tornado.web
import tornado.websocket

PORT = 8888


class MainHandler(tornado.web.RequestHandler):
    """
    Base handler to the main page.
    """

    def get(self):
        self.render("templates/index.html")


class MessageHandler(tornado.web.RequestHandler):
    """
    Handler for the messages sent by POST.
    """

    def post(self):
        message = self.get_argument("message")
        BroadCastHandler.broadcast(message)
        self.redirect("/")


class BroadCastHandler(tornado.websocket.WebSocketHandler):
    """
    Handler that broadcasts the messages received.
    """

    connections = set()

    @classmethod
    def broadcast(cls, message):
        for connection in cls.connections:
            try:
                connection.write_message(message)
            except Exception as exc:
                print(f"Fail to send message: {exc}")

    def open(self):
        """
        Add connection to the set when a new connection is established.
        """
        self.connections.add(self)

    def on_close(self):
        """
        Remove connection when the websocket is closed.
        """
        self.connections.remove(self)


class WebSocketConnectionHandler(tornado.web.RequestHandler):
    """
    Handler for the page the receives the messages.
    """

    def get(self):
        self.render("templates/broadcast.html")


def make_app():
    return tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/messages", MessageHandler),
            (r"/broadcast", WebSocketConnectionHandler),
            (r"/web_socket_broadcast", BroadCastHandler),
        ]
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(PORT)
    tornado.ioloop.IOLoop.current().start()
