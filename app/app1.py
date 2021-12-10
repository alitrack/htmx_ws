from flask import Flask,json
from flask.templating import render_template
from flask_sockets import Sockets
import datetime
import time
import random

from geventwebsocket.websocket import WebSocket

from werkzeug.routing import Rule


app = Flask(__name__)
sockets = Sockets(app)

#https://github.com/heroku-python/flask-sockets/issues/81
@sockets.route('/ws', websocket=True)
def echo_socket(ws:WebSocket):
    while not ws.closed:
        msg = ws.read_message()
        if msg:
            msg = json.loads(msg)
            content = """
            <div hx-swap-oob="beforeend:#content">
            <p>{time}: {message}</p>
            </div>
            """
            ws.send(
                    content.format(time=time.time(), message=msg["chat_message"])
                )
        


sockets.url_map.add(Rule('/ws', endpoint=echo_socket, websocket=True))


@app.route('/')
async def hello():
    return render_template("index.html")


if __name__ == "__main__":
    # app.run()
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 8001), app, handler_class=WebSocketHandler)
    print('server start')
    server.serve_forever()