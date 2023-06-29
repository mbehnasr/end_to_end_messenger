#!/usr/bin/env python

import asyncio
import websockets
import uuid
import json
client_uuid = str(uuid.uuid4())

async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while True:

            name = input("What's your name? ")

            data = {
                'userId': name+client_uuid,
                'uuid': client_uuid,
            }
            data_string = json.dumps(data)
            await websocket.send(data_string)
            print(f">>> {name}")

            greeting = await websocket.recv()
            print(f"<<< {greeting}")    

async def main():
    async with websockets.serve(hello, "localhost", 8765):
        await asyncio.Future()  # run forever
if __name__ == "__main__":
    asyncio.run(hello()) 