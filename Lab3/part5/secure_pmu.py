import socket
import sys
import ssl
import random

if len(sys.argv) == 4:
    port = int(sys.argv[1])
    cert = sys.argv[2]
    key = sys.argv[3]
    print("Arguments:",port,cert,key)
else:
    print("Wrong number of arguments:", len(sys.argv))
    sys.exit(1)

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=cert, keyfile=key)
    context.load_verify_locations("Part5_ca.crt")

    sock.bind(('0.0.0.0', port))
    sock.listen(1)
    print(f"Listening on port {port}...", flush=True)

    conn, addr = sock.accept()
    print(f"Connection from {addr}", flush=True)

    tls_conn = context.wrap_socket(conn, server_side=True)

    data = tls_conn.recv(1024).decode().strip()
    print(f"Received command: {data}", flush=True)  

    if data.startswith("CMD_short:"):
        for i in range(random.randint(3, 10)):
            msg = f"This is PMU data {i}\n"
            tls_conn.sendall(msg.encode())
    else:
        print("Unexpected command:", data, flush=True)



except KeyboardInterrupt:
    print("\nInterrupted by user.")
except Exception as e:
    print(f"Error: {e}",flush=True)
finally:
    try:
        tls_conn.shutdown(socket.SHUT_RDWR)
        tls_conn.close()
    except:
        pass
    sock.close()
    print("Socket closed.")