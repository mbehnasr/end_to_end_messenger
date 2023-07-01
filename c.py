#!/usr/bin/env python

import asyncio
import websockets
import uuid
import json
client_uuid = str(uuid.uuid4())
import threading
from threading import Thread, Lock


from Crypto.PublicKey import RSA
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()
# public_key and private_key generator

"""
create session key for client chat with each other
from Crypto.Cipher import AES

file_in = open("encrypted.bin", "rb")
nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]
file_in.close()

# let's assume that the key is somehow available again
cipher = AES.new(key, AES.MODE_EAX, nonce)
data = cipher.decrypt_and_verify(ciphertext, tag)
 """


async def receiver_async(websocket):
    while True:
            receive_message = await websocket.recv()
            receive_message_json = json.loads(receive_message)
            print(receive_message)

def receiver(websocket):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(receiver_async(websocket))
    loop.close()

def sender(websocket):
    while True:
        print("client")
#         options = input("\nEnter number you wana do :\n 1-send message:\n 2-exit:")
#         if(options == 1):
        target_user = input("\nEnter target user UUID:\n")

        message = {}
        message["type"] = "send_message"
        message["target_user"] = target_user
        message["message"] = "I wana connect to another person"
        message["public_key"] = str(public_key)
        type(public_key)
        websocket.send(json.dumps({"type":"send_message","target_user":target_user,"message":"I wana connect to another person","public_key":str(public_key),"sender_user":client_uuid}))


async def hello():
    uri = "ws://localhost:8765"

    async with websockets.connect(uri) as websocket:
        data = {
            'userId': client_uuid,
            'uuid': client_uuid,
        }
        data_string = json.dumps(data)

        await websocket.send(data_string)
        users = await websocket.recv()
        users_json =  json.loads(users)

        for user in users_json:
            keys = user.keys()
            for key in keys:
                print(key)

        print("before")
        send_thread = threading.Thread(target=sender(websocket), args=(1,))

        recv_thread = threading.Thread(target=receiver(websocket), args=(1,))
        print("after")




async def main():
    async with websockets.serve(hello, "localhost", 8765):
        await asyncio.Future()  # run forever
if __name__ == "__main__":
    asyncio.run(hello()) 