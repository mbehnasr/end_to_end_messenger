import asyncio
import json
import websockets
import uuid

client_uuid = str(uuid.uuid4())


async def save_uuid():
    # Save the client's UUID to a JSON file
    data = {client_uuid: "fuck"}
    with open("uuid.json", "w") as file:
        json.dump(data, file)


async def send_message():
    target_uuid = input("Enter the target UUID: ")
    content = input("Enter the message content: ")

    message = {
        "target_uuid": target_uuid,
        "content": content
    }
    message_json = json.dumps(message)

    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send(client_uuid)
        await websocket.send(message_json)


async def main():
    await save_uuid()
    await send_message()


asyncio.run(main())
