import asyncio
import websockets


async def receive_messages():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            print(f"Received message: {message}")


async def send_messages():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            message = input("Enter a message to send: ")
            await websocket.send(message)


async def main():
    # Run both receiving and sending messages concurrently
    await asyncio.gather(receive_messages(), send_messages())


asyncio.run(main())
