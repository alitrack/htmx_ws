import socketio

sio = socketio.Client()
sio.connect('ws://127.0.0.1:8001',  wait=True, wait_timeout= 5)
for i in range(10):
    sio.emit("send",data={"data":"message","i":i})
# sio.disconnect()