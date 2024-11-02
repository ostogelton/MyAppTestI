import socket
import cv2
import pickle
import struct

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 9999))  # Bind to all interfaces on port 9999
server_socket.listen(1)
print("Server listening...")

# Accept a connection
client_socket, addr = server_socket.accept()
print(f"Connection from: {addr}")

# Start capturing video
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Serialize and send the frame
    data = pickle.dumps(frame)
    size = struct.pack("Q", len(data))
    client_socket.sendall(size + data)

# Cleanup
cap.release()
client_socket.close()
server_socket.close()