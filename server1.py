import asyncio
import json
import websockets

# Dictionary to store connected clients with their UUIDs
clients = {}


async def handle_message(message, sender_uuid):
    parsed_message = json.loads(message)
    target_uuid = parsed_message["target_uuid"]
    content = parsed_message["content"]

    if target_uuid in clients:
        target_client = clients[target_uuid]
        await target_client.send(content)


async def handle_client(websocket, path):
    # Receive the client's UUID and store it in the dictionary
    uuid = await websocket.recv()
    clients[uuid] = websocket

    try:
        async for message in websocket:
            await handle_message(message, uuid)
    finally:
        # Remove the client from the dictionary when they disconnect
        del clients[uuid]


async def main():
    # Start the WebSocket server
    async with websockets.serve(handle_client, "localhost", 8765):
        await asyncio.Future()  # Keep the server running


asyncio.run(main())
