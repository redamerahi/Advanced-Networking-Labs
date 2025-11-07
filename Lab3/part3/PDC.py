import socket
import sys

#____________PDC (Phasor Data Concentrator)____________#

# Check command-line arguments
if len(sys.argv) == 3:
    server = sys.argv[1]
    port = int(sys.argv[2])
    print("Arguments:", server, port)
else:
    print("Wrong number of arguments:", len(sys.argv))
    sys.exit(1)

try:
    # Create UDP sockets for IPv4 and IPv6
    sock4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock4.settimeout(1.0)
    sock6.settimeout(1.0)

    # Resolve both IPv4 and IPv6 addresses 
    ipv4_addr = None
    ipv6_addr = None
    addr = socket.getaddrinfo(server, port, 0, socket.SOCK_DGRAM)

    for info in addr:
        family, socktype, proto, canonname, sockaddr = info
        if family == socket.AF_INET:
            ipv4_addr = sockaddr
        elif family == socket.AF_INET6:
            ipv6_addr = sockaddr

    print(f"Resolved IPv4 address: {ipv4_addr}")
    print(f"Resolved IPv6 address: {ipv6_addr}")

    if not ipv4_addr and not ipv6_addr:
        print("No valid IPv4 or IPv6 address found.")
        sys.exit(1)

    # Prepare the RESET message
    message = "RESET:20".encode()

    print("Sending RESET:20 requests to server...")

    # Main loop: keep sending until response is received
    while True:
        
        # Send the message on both IPv4 and IPv6
        if ipv4_addr:
            sock4.sendto(message, ipv4_addr)
        if ipv6_addr:
            sock6.sendto(message, ipv6_addr)

        # Try to receive a response from either socket
        try:
            data, addr = sock4.recvfrom(1024)
        except socket.timeout:
            try:
                data, addr = sock6.recvfrom(1024)
            except socket.timeout:
                print("No response, retrying ...")
                continue

        # Process the received message
        text = data.decode().strip()
        print(f"Received {text} from {addr}")
        break

    print("Reset ACK. Exiting!")

except KeyboardInterrupt:
    print("\nInterrupted by user.")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Always close sockets before exiting
    if sock4:
        sock4.close()
    if sock6:
        sock6.close()
    print("Sockets closed.")
