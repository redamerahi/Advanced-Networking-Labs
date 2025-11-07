import socket
import sys
import time

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
    message = b"RESET:20"

    # Parameters for the experiment
    num_tests = 60
    attempt_counts = []

    print(f"\nRunning {num_tests} tests...\n")

    # Loop for 60 trials
    for test in range(1, num_tests + 1):
        attempts = 0
        while True:
            attempts += 1

            # Send on both IPv4 and IPv6
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
                    print(f"[Test {test}] No response (attempt {attempts}), retrying...")
                    continue

            # Process received message
            text = data.decode().strip()
            print(f"[Test {test}] Received {text} after {attempts} attempts from {addr}")
            break

        # Store number of attempts for this test
        attempt_counts.append(attempts)
        # Small delay between tests to avoid flooding
        time.sleep(0.5)

    # Compute statistics
    avg_attempts = sum(attempt_counts) / len(attempt_counts)
    success_prob = 1 / avg_attempts
    loss_prob = 1 - success_prob

    print("\n--- Results ---")
    print(f"Attempts per test: {attempt_counts}")
    print(f"Average attempts before acknowledgment: {avg_attempts:.2f}")
    print(f"Estimated success probability p: {success_prob:.3f}")
    print(f"Estimated loss probability: {loss_prob:.3f}")

except KeyboardInterrupt:
    print("\nInterrupted by user.")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Always close sockets before exiting
    if 'sock4' in locals():
        sock4.close()
    if 'sock6' in locals():
        sock6.close()
    print("Sockets closed.")
