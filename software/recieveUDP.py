import socket

# Configure the server
UDP_IP = "0.0.0.0"  # Listen on all available interfaces
UDP_PORT = 5005     # Same as the port used on the iPhone

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for UDP messages on {UDP_IP}:{UDP_PORT}...")

try:
    while True:
        data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
        print(f"Received message: {data.decode('utf-8')} from {addr}")
except KeyboardInterrupt:
    print("\nServer shutting down...")
finally:
    sock.close()
