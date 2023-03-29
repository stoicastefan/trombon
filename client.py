import asyncio
import websockets


async def test():
    async with websockets.connect('http://localhost:63342/trombon_server/index.html?_ijt=jk0tt2t3drct3476aqrp188vus&_ij_reload=RELOAD_ON_SAVE') as websocket:
        await websocket.send("hello")
        response = await websocket.recv()
        print(response)


asyncio.get_event_loop().run_until_complete(test())