import websocket
import sys

#____________ PDC (Phasor Data Concentrator) using WebSocket ____________#

if len(sys.argv) == 4:
    server = sys.argv[1]
    port = int(sys.argv[2])
    command = sys.argv[3]
    print("Arguments:", server, port, command, flush=True)
else:
    print("Wrong number of arguments:", len(sys.argv), flush=True)
    sys.exit(1)

try:
    url = f"ws://{server}:{port}"
    ws = websocket.create_connection(url)
    print(f"Connected to {url}", flush=True)

    ws.send(command)
    print(f"Sent command: {command}", flush=True)

    while True:
        data = ws.recv()
        if isinstance(data, bytes):
            data = data.decode()
        print(data.strip(), flush=True)

except KeyboardInterrupt:
    print("\nInterrupted by user.", flush=True)
except websocket._exceptions.WebSocketConnectionClosedException:
    print("Connection closed by server.", flush=True)
except Exception as e:
    print(f"Error: {e}", flush=True)
finally:
    if 'ws' in locals():
        ws.close()
    print("Socket closed.", flush=True)
