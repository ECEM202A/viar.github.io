import socket

UDP_IP = "192.168.1.123"  # Replace with iPhone's local IP address
UDP_PORT = 5005
MESSAGE = "this is Ethan"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
print(f"Sent: {MESSAGE}")
