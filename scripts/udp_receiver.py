import socket
import threading

class UDPReceiver:
    """
    A simple UDP receiver that listens for incoming data on a specified port.
    Optionally accepts a callback function to handle received data.
    """

    def __init__(self, port: int, buffer_size: int = 1024, encoding: str = 'ascii'):
        self.port = port
        self.buffer_size = buffer_size
        self.encoding = encoding
        self._sock = None
        self._running = False
        self._thread = None
        self._callback = None

    def start(self, callback=None):
        """
        Start listening for UDP packets. Optionally provide a callback function.
        The callback receives one argument: the decoded string data.
        """
        if self._running:
            raise RuntimeError("Receiver is already running.")

        self._callback = callback
        self._running = True
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind(("127.0.0.1", self.port))
        print(f"[UDPReceiver] Listening on port {self.port}...")

        self._thread = threading.Thread(target=self._listen, daemon=True)
        self._thread.start()

    def _listen(self):
        while self._running:
            try:
                data, addr = self._sock.recvfrom(self.buffer_size)
                if data:
                    decoded = data.decode(self.encoding, errors='replace')
                    if self._callback:
                        self._callback(decoded)
                    else:
                        print(decoded, end='')
            except Exception as e:
                if self._running:
                    print(f"[UDPReceiver] Error: {e}")

    def stop(self):
        """
        Stop listening and close the socket.
        """
        if not self._running:
            return

        self._running = False
        if self._sock:
            self._sock.close()
        print(f"[UDPReceiver] Stopped listening on port {self.port}.")

    def is_running(self):
        """Return True if the receiver is active."""
        return self._running
