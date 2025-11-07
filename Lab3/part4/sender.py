import socket
import sys
import struct

if len(sys.argv) == 4:
    group = sys.argv[1]
    port = int(sys.argv[2])
    sciper = sys.argv[3]
    print("Arguments:", group,port,sciper)
else:
    print("Wrong number of arguments:", len(sys.argv))
    sys.exit(1)

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    
    while True:
        message = input("> ")
        packet = sciper.encode() + message.encode()
        sock.sendto(packet, (group, port))


except KeyboardInterrupt:
    print("\nInterrupted by user.")
except Exception as e:
    print(f"Error: {e}")
finally:
    sock.close()
    print("Socket closed.")