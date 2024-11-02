import socket
import cv2
import pickle
import struct
from kivy import app
from kivy.app import App
from kivy.uix.label import Label


class MyApp(App):
    # Create a socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.5.104', 9999))  # Replace 'SERVER_IP' with the server's IP address

    data = b""
    payload_size = struct.calcsize("Q")


    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4 * 1024)  # Receive packets
            if not packet:
                break
            data += packet

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += client_socket.recv(4 * 1024)

        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)

        cv2.imshow("Receiving Video", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    client_socket.close()
if __name__ == '__main__':
    MyApp().run()