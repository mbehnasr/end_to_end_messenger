#!/usr/bin/env python

import asyncio
import datetime
import random
import websockets
import json
import os
import logging
# logger = logging.getLogger('websockets')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())

users=[]

CONNECTIONS = set()
# USERS = "./users.json"
async def save_user(user, websocket):
    global USERS
    try:
        new_user = {
            user["uuid"]: str(websocket),
        }

        with open('./users.json') as file:
            json_data = json.load(file)

        json_data.append(new_user)
        print(json_data)
        with open('users.json', 'w') as file:
               json.dump(json_data, file)
#         await asyncio.sleep(random.random() * 2 + 10)
        websockets.broadcast(CONNECTIONS, json.dumps(json_data.append({"type": "users"})))

        print(f"Received and saved file: {new_user}")
    except json.JSONDecodeError as e:
        print(f"Invalid JSON format: {e}")




async def register(websocket):
    print(websocket)
    print("\n")
    print(id(websocket))
    CONNECTIONS.add(websocket)
    print(CONNECTIONS)
    new_user = await websocket.recv()
    new_user = json.loads(new_user)
    print(new_user["uuid"])
    await save_user(new_user , websocket)

    try:

        await websocket.wait_closed()
    finally:
        CONNECTIONS.remove(websocket)




async def show_time():
    while True:
        message = datetime.datetime.utcnow().isoformat() + "Z"
        websockets.broadcast(CONNECTIONS, message)
        await asyncio.sleep(random.random() * 2 + 1)



async def main():
    async with websockets.serve(register, "localhost", 8765):
        await show_time()

if __name__ == "__main__":
    asyncio.run(main())