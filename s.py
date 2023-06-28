#!/usr/bin/env python

import json
import asyncio
import websockets

CONNECTIONS = set()


async def register(websocket):
    CONNECTIONS.add(websocket)
    print("all CONNECTIONS", CONNECTIONS)
    try:
        await websocket.wait_closed()
    finally:
        CONNECTIONS.remove(websocket)

async def hello(websocket):
    name = await websocket.recv()
    print(f"<<< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f">>> {greeting}")

async def main():
    async with websockets.serve(hello, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())