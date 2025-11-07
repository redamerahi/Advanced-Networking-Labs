import socket
import sys
import re 

#____________PDC (Phasor Data Concentrator)____________#

if len(sys.argv) == 4:

    server = sys.argv[1]
    port = int(sys.argv[2])
    command = sys.argv[3]

    if command not in ["CMD_short:0","CMD_short:1","CMD_floodme"]:
        print("Wrong command in arument !")
        sys.exit(1)
    
    #print("Arguments : ",server,port,command)

else:
    print("Wrong number of arguments :",len(sys.argv))
    sys.exit(1)

try:

    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((server,port))
    sock.sendall(command.encode())

    buffer = "" 
    MARKER = "This is PMU data "
    #recv_count = 0  

    while True:
        data = sock.recv(1024)
        #recv_count += 1 
        if data == b'':
            break
        buffer += data.decode()

        index = 0
        while index < len(buffer):
            # Look for a digit
            if buffer[index].isdigit():
                num = buffer[index]
                i = index + 1

                # Read all following digits (to handle multi-digit numbers)
                while i < len(buffer) and buffer[i].isdigit():
                    num += buffer[i]
                    i += 1

                # If we reached the end of the buffer while reading digits,
                # it means the message was cut in half by TCP (incomplete number)
                if i == len(buffer):
                    # Keep the partial number and everything after it
                    buffer = buffer[index:]
                    break

                # Full number found: print it immediately
                print(MARKER + num)

                # Remove everything that has already been processed
                buffer = buffer[i:]
                index = 0  # restart parsing from the beginning of the new buffer
                continue

            index += 1

    if buffer: #last number remaining in the buffer (in this case buffer = [1,1])
        print(MARKER + buffer)

except KeyboardInterrupt:
    print("\nInterrupted by user.")
except Exception as e:
    print(f"Error: {e}")
finally:
    #print(f"Number of recv() calls: {recv_count}")
    sock.close()




