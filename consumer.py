import asyncio
import logging
import websockets

logger = logging.getLogger()


""" Функция принимает адрес и подключает к нему клиента """


async def consume(min_value: int, max_value: int, hostname: str, port: int) -> None:
    url = f"ws://{hostname}:{port}"
    async with websockets.connect(url) as websocket:
        await consumer_handler(websocket, min_value, max_value)
        
        
""" Функция принимает сообщения и отправляет их на проверку """


async def consumer_handler(websocket: websockets.WebSocketClientProtocol,
                           min_value: int, max_value: int) -> None:
    async for message in websocket:
        if check_the_num(message, min_value, max_value):
            log_message(message)
            
        
""" Функция отвечает за логирование """


def log_message(message: str) -> None:
    logger.info(message)


""" Функция парсит сообщение и проверяет число """


async def check_the_num(message: str, min_value: int, max_value: int) -> bool:
    dict_message = eval(message)
    for integer in dict_message.values:
        if integer < min_value or integer > max_value:
            return True


if __name__ == '__main__':
    min_num = int(input('Нижний порог: '))
    max_num = int(input('Верхний порог: '))
    logging.basicConfig(
        level=logging.INFO,
        filename='random_nums.log',
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume(min_value=min_num, max_value=max_num, hostname='localhost', port=5000))
    loop.run_forever()