import socket
import sys
import struct

# Check command-line arguments
if len(sys.argv) == 3:
    group = sys.argv[1]
    port = int(sys.argv[2])
    print("Arguments:", group, port)
else:
    print("Wrong number of arguments:", len(sys.argv))
    sys.exit(1)

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', port))

    mreq = struct.pack("4s4s",socket.inet_aton(group),socket.inet_aton("0.0.0.0"))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"Listening on multicast group {group}:{port}")
    
    while True:
        data, addr = sock.recvfrom(1024)
        print(data.decode().strip())

except KeyboardInterrupt:
    print("\nInterrupted by user.")
except Exception as e:
    print(f"Error: {e}")
finally:
    sock.close()
    print("Socket closed.")