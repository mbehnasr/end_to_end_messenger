import asyncio
import websockets

# Dictionary to store connected clients
clients = set()


async def handle_message(message, sender):
    # Broadcast the received message to all connected clients except the sender
    for client in clients:
        if client != sender:
            await client.send(message)


async def handle_client(websocket, path):
    # Add the client to the set of connected clients
    clients.add(websocket)

    try:
        async for message in websocket:
            print(message)
            print(clients)
            await handle_message(message, websocket)
    finally:
        # Remove the client from the set when they disconnect
        clients.remove(websocket)


async def main():
    # Start the WebSocket server
    async with websockets.serve(handle_client, "localhost", 8765):
        await asyncio.Future()  # Keep the server running


asyncio.run(main())
