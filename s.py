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



CONNECTIONS = set()
USERS = "users.json"
async def save_user(user):
    try:
        """ new_user = {
            [user[uuid]]: user[userId]
        }

        users = json.dumps(USERS)
        users.append(new_user)

        with open(USERS, "w") as file:
            json.dump(users, file, indent=4)
 """
        print("omad tosh")
        print(f"Received and saved file: {userId}")
    except json.JSONDecodeError as e:
        print(f"Invalid JSON format: {e}")




async def register(websocket):
    print(websocket)
    print("\n")
    print(id(websocket))
    CONNECTIONS.add(websocket)
    print(CONNECTIONS)
    try:
        new_user = await websockets.recv()
        new_user = json.loads(new_user)
        print(new_user)
        await register(new_user["uuid"])
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