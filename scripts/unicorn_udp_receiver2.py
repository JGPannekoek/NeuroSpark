import socket

def main():
    print("Unicorn Recorder UDP Receiver Example")
    print("----------------------------\n")
    
    try:
        # Ask for destination port
        port = int(input("Destination port: "))
        print(f"Listening on port '{port}'...")
        
        # Bind UDP socket to all interfaces (like IPAddress.Any)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("127.0.0.1", port))  # listen on all interfaces
        
        # Buffer for receiving data
        buffer_size = 1024
        receive_buffer = bytearray(buffer_size)
        
        print("Acquisition loop started. Press Ctrl+C to exit.\n")
        
        while True:
            data, addr = sock.recvfrom(buffer_size)
            if data:
                # Print as ASCII (like C# Encoding.ASCII)
                print(data.decode('ascii', errors='replace'), end='')
                
                # Optional: clear buffer (not strictly needed in Python)
                receive_buffer[:] = b'\x00' * buffer_size
                
    except Exception as ex:
        print(f"Error: {ex}")
        input("Press ENTER to terminate the application.")

if __name__ == "__main__":
    main()
