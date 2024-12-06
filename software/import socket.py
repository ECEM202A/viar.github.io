# import socket

# UDP_IP = "192.168.1.123"  
# UDP_PORT = 5005
# MESSAGE = "Hello from Laptop"

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
# print(f"Sent: {MESSAGE}")
import socket

UDP_IP = "131.179.44.189" 
UDP_PORT = 53
MESSAGE = ""

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
print(f"Sent: {MESSAGE} to {UDP_IP}:{UDP_PORT}")
