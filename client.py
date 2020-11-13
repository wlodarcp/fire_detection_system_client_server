# -*- coding: utf-8 -*-
import cv2
import numpy as np
import socket
import pickle
import struct

cap=cv2.VideoCapture(0)
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('localhost',8098))

while True:
    ret,frame=cap.read()
    # Serialize frame
    data = pickle.dumps(frame)
    # Send message length first
    message_size = struct.pack("L", len(data))
    is_fire = struct.pack("?", True)
    # Then data
    clientsocket.sendall(is_fire + message_size + data)
    
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
    
cap.release()  
clientsocket.stop()
    
