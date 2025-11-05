import socket

def main():
    print("Unicorn Recorder UDP Receiver Example")
    print("----------------------------\n")

    try:
        # Ask for destination port
        port = int(input("Destination port: "))
        print(f"Listening on port '{port}'...")

        # Create a UDP socket and bind it to the requested port on all interfaces
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", port))

        # Buffer for receiving data
        buffer_size = 1024
        print("check")

        # Acquisition loop
        while True:
            print("Waiting for UDP packet...")
            sock.settimeout(5)  
            # data, addr = sock.recvfrom(buffer_size)
            # print(f"Received {len(data)} bytes from {addr}")
            try:
                data, addr = sock.recvfrom(buffer_size)
                print(f"Received {len(data)} bytes from {addr}")
            except socket.timeout:
                print("No data received in 5 seconds")
                
            if data:
                # try to decode as ASCII and print; on failure, print a safe representation
                try:
                    print(data.decode('ascii', errors='replace'), end='')
                except Exception:
                    print(repr(data))

    except Exception as ex:
        print(f"Error: {ex}")
        input("Press ENTER to terminate the application.")

if __name__ == "__main__":
    main()