# -*- coding: utf-8 -*-
import cv2
import numpy as np
import socket
import sys
import pickle
import struct


video = "flame2.mp4"
# odkomentować w celu testów pliku wideo na dysku
cap = cv2.VideoCapture(video)
# odkomentować w celu testów z k

clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('localhost',8010))

while True:
    ret,frame=cap.read()
    # Serialize frame
    data = pickle.dumps(frame)

    # Send message length first
    message_size = struct.pack("L", len(data)) ### CHANGED

    # Then data
    clientsocket.sendall(message_size + data)