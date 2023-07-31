import urllib

import tornado
from tornado.testing import AsyncHTTPTestCase
from tornado.websocket import websocket_connect
from tornado.ioloop import IOLoop

from broadcast_server import make_app


class TestApplication(AsyncHTTPTestCase):
    WEBSOCKET_URL = "ws://localhost:8888/web_socket_broadcast"
    TEST_MESSAGE = "This is a message"

    def get_app(self):
        return make_app()

    def test_that_we_can_send_a_message(self):
        body = urllib.parse.urlencode({"message": "Hey, how are you!"})
        response = self.fetch("/messages", method="POST", body=body)
        self.assertEqual(response.code, 200)

    def test_websocket_broadcast(self):
        websocket_url = self.WEBSOCKET_URL
        websocket_client = websocket_connect(websocket_url)
        websocket = IOLoop.current().run_sync(lambda: websocket_client)

        websocket.write_message(self.TEST_MESSAGE)
        response = IOLoop.current().run_sync(websocket.read_message)
        self.assertEqual(response, self.TEST_MESSAGE)


if __name__ == "__main__":
    tornado.testing.main()
