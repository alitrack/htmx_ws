import time

from fastapi import FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")


app = FastAPI()


@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def time_handler(websocket: WebSocket):
    await websocket.accept()
    # response content
    content = """
        <div hx-swap-oob="beforeend:#content">
        <p>{time}: {message}</p>
        </div>
    """
    while True:
        msg = await websocket.receive_json()
        await websocket.send_text(
            content.format(time=time.time(), message=msg["chat_message"])
        )