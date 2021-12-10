from flask import Flask, render_template,request
from flask_socketio import SocketIO, emit

import time


# from gevent import monkey
# monkey.patch_all()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['DEBUG'] = True

sio = SocketIO(app,cors_allowed_origins="*",async_mode="gevent"
                ,source="ws",namespace="/")

@app.route('/')
def index():
    return render_template('index.html')


@sio.on('send')
def ws_message(message):
    # emit('my response', {'data': message['data']})
    # response content
    print(message)
    content = """
        <div hx-swap-oob="beforeend:#content">
        <p>{time}: {message}</p>
        </div>
    """
    while True:
        sio.emit("send",
            content.format(time=time.time(), message=message["chat_message"],namespace="/")
        )    

@sio.event
def connect():
    print('connect ')

@sio.event
def disconnect():
    print('disconnect ')

@sio.on("send")
def send(json):
    print("send",json)
@sio.on("message")
def message(json):
    print("message",json)    

if __name__ == '__main__':

    sio.run(app,debug=True,port=8001)