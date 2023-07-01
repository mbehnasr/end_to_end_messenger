#!/usr/bin/env python

import asyncio
import datetime
import random
import websockets
import json
import os
import logging
import threading


#Beine in file va file baadi byd amaliate tabadole session key anjam she.
# logger = logging.getLogger('websockets')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())
"""
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

data = b'secret data'

key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_EAX)
ciphertext, tag = cipher.encrypt_and_digest(data)

file_out = open("encrypted.bin", "wb")
[ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]
file_out.close()
 """

"""
from Crypto.PublicKey import RSA

key = RSA.generate(2048)
private_key = key.export_key()
file_out = open("private.pem", "wb")
file_out.write(private_key)
file_out.close()

public_key = key.publickey().export_key()
file_out = open("receiver.pem", "wb")
file_out.write(public_key)
file_out.close()
#Beine in file va file baadi byd amaliate tabadole session key anjam she.
"""

CONNECTIONS = set()
connected_clients = {}

SEND_MESSAGE_TO_ANOTHER = "send_message"
TARGET_USER = "target_user"


async def save_user(user, websocket):
    try:
        new_user = {
            user["uuid"]: str(websocket),
        }
        connected_clients[user["uuid"]] = websocket

        with open('./users.json') as file:
            json_users = json.load(file)
        json_users_with_new_user = json_users
        json_users_with_new_user.append(new_user)


        with open('users.json', 'w') as file:
               json.dump(json_users_with_new_user, file)
#         await asyncio.sleep(random.random() * 2 + 10)
#         websockets.broadcast(CONNECTIONS, json.dumps(json_data.append({"type": "users"})))
        for socket in CONNECTIONS:
#             await socket.send("is connected")
            await socket.send(str(CONNECTIONS))
    except json.JSONDecodeError as e:
        print(f"Invalid JSON format: {e}")




async def register(websocket):

    CONNECTIONS.add(websocket)
    client_id = id(websocket)
    connected_clients[client_id] = websocket

    new_user = await websocket.recv()
    new_user = json.loads(new_user)

    await save_user(new_user , websocket)


    await communicate(websocket)
    try:
        await websocket.wait_closed()
    finally:
        CONNECTIONS.remove(websocket)
        connected_clients.pop(client_id, None)

async def receiver_async(websocket):
    while True:
        message = await websocket.recv()
        message_json = json.loads(message)
        if(message_json["type"] == SEND_MESSAGE_TO_ANOTHER):
            """ with open('./users.json') as file:
                json_users = json.load(file)
            print(type(json_users))
            print(json_users)
            print(connected_clients[message_json["target_user"]]) """

            print("sender_user :" , message_json["sender_user"])
            websocket_target_user = connected_clients.get(message_json["target_user"])
            print("target_user: ", message_json["target_user"])
            await websocket_target_user.send("sd")

def receiver(websocket):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(receiver_async(websocket))
    loop.close()


#         message = datetime.datetime.utcnow().isoformat() + "Z"
#         websockets.broadcast(CONNECTIONS, message)
#         await asyncio.sleep(random.random() * 2 + 1)



async def communicate(websocket):
    print("before recv_thread done")
    recv_thread = threading.Thread(target=receiver(websocket), args=(1,))
    print("after recv_thread done")


"""
async def say_hello():
    while True:
        for socket in CONNECTIONS:
            socket.send("hello")

"""




# async def main():
#     async with websockets.serve(register, "localhost", 8765):
start_server = websockets.serve(register, 'localhost', 8765)
loop = asyncio.get_event_loop()


try:
    loop.run_until_complete(start_server)
    loop.run_forever()
finally:
    loop.close()
# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()
#         await show_time()
#         await say_hello()

# if __name__ == "__main__":
#     asyncio.run(main())