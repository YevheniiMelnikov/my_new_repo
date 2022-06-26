import datetime
import json
import random
import asyncio
import websockets
from typing import Coroutine
from server import Server


""" Функция отправляет json на сервер """


async def produce(message: Coroutine, host: str, port: int, sleep: int):
    async with websockets.connect(f"ws://{host}:{port}") as ws:
        await ws.send(message)
        await ws.recv()
        await asyncio.sleep(sleep)


""" Функция создает json """


async def json_generator():
    ts = datetime.datetime.now().timestamp()
    num = random.randint(1, 100)
    data = {ts: num}
    message = json.dumps(data)
    return message
  
    
if __name__ == '__main__':
    frequency = int(input('Скорость отправки: '))
    server = Server()
    start_server = websockets.serve(server.ws_handler, 'localhost', 5000)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_until_complete(produce(message=json_generator(), host='localhost', port=5000, sleep=frequency))
    loop.run_forever()