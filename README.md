# tornado_playground
This is my repo to play with Tornado.

## Broadcast using WebSockets

This simple application receives messages from a POST request and broadcasts to all websocket connections opened.

### Demo

https://github.com/aemitos/tornado_playground/assets/1443757/c9c1758a-bdbd-4448-8f4e-a04cbc455ca2

### Running instructions

```bash
$ cd ~/<your repos directory>/tornado_playground
$ virtualenv venv ; source venv/bin/activate
(venv) $ pip install -r requirements.txt
(venv) $ cd websockets_broadcast
(venv) $ python broadcast_server.py
```

Open your browser and access [http://localhost:8888](http://localhost:8888) and open a broadcast page in another tab. Send messages and see them on the opened tab.
