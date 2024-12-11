import socket

UDP_IP = "192.168.1.123" 
UDP_PORT = 53
MESSAGE = "Right"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
print(f"Sent: {MESSAGE} to {UDP_IP}:{UDP_PORT}")
