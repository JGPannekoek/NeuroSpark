import socket

def main():
    print("Unicorn Recorder UDP Receiver Example")
    print("----------------------------\n")

    try:
        # Ask for destination port
        port = int(input("Destination port: "))
        print(f"Listening on port '{port}'...")

        # Create a UDP socket and bind it to all interfaces
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", port))

        # Buffer for receiving data
        buffer_size = 1024

        # Acquisition loop
        while True:
            data, addr = sock.recvfrom(buffer_size)
            if data:
                print(data.decode('ascii', errors='replace'), end='')

    except Exception as ex:
        print(f"Error: {ex}")
        input("Press ENTER to terminate the application.")

if __name__ == "__main__":
    main()