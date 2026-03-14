import socket
import mss
import cv2
import numpy as np
import pickle
import struct

host = "0.0.0.0"
port = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)

print("Waiting for connection...")

conn, addr = server_socket.accept()
print("Connected:", addr)

with mss.mss() as sct:
    monitor = sct.monitors[1]

    while True:
        img = np.array(sct.grab(monitor))
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        data = pickle.dumps(img)
        message = struct.pack("Q", len(data)) + data
        conn.sendall(message)