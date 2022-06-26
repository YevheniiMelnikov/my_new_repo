import asyncio
from websockets import WebSocketServerProtocol


class Server:
    clients = set()
    
    async def register(self, ws: WebSocketServerProtocol) -> None:
        self.clients.add(ws)
    
    async def unregister(self, ws: WebSocketServerProtocol) -> None:
        self.clients.remove(ws)
        
    async def send(self, message: str) -> None:
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients])
            
    async def ws_handler(self, ws: WebSocketServerProtocol, url: str) -> None:
        await self.register(ws)
        try:
            await self.distribute(ws)
        finally:
            await self.unregister(ws)
            
    async def distribute(self, ws: WebSocketServerProtocol) -> None:
        async for message in ws:
            await self.send(message)
