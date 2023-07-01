#!/usr/bin/env python

import asyncio
import websockets
import uuid
import json
client_uuid = str(uuid.uuid4())

from Crypto.PublicKey import RSA
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()


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
#Beine in file va file baadi byd amaliate tabadole session key anjam she. """


async def hello():
    uri = "ws://localhost:8765"

    async with websockets.connect(uri) as websocket:

        data = {
            'userId': client_uuid,
            'uuid': client_uuid,
        }
        data_string = json.dumps(data)

        await websocket.send(data_string)
        send_okaye = await websocket.recv()
        users = await websocket.recv()
        users_json =  json.loads(users)


        for user in users_json:
            keys = user.keys()
            for key in keys:
                print(key)


        while True:
            target_user = input("\ninput target user:\n")
            print(f">>> {target_user}")
            message = {}
            message["type"] = "send_message"
            message["target_user"] = target_user
            message["message"] = "I wana connect to another person"
            message["public_key"] = public_key
            type(public_key)

            await websocket.send(json.dumps({"type":"send_message","target_user":target_user,"message":"I wana connect to another person","public_key":str(public_key)}))

            answer = await websocket.recv()
            print(f"<<< {answer}")

async def main():
    async with websockets.serve(hello, "localhost", 8765):
        await asyncio.Future()  # run forever
if __name__ == "__main__":
    asyncio.run(hello()) 