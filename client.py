# -*- coding: utf-8 -*-
import pickle
import socket
import struct
import os
import cv2
import numpy as np
from keras.preprocessing import image

from ArgumentParaser import parase_arguments
from FireDetectionModel import load_model, img_width, img_height
from VideoSourceProvider import get_video_capture

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def connect_to_server_socket(HOST, port):
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((HOST, port))
    return clientsocket


def stream_video_with_fire_detection_signal(cap, clientsocket):
    fire_detection_model = load_model('model2.h5')
    while True:
        ret, frame = cap.read()
        resized_frame = cv2.resize(frame, (img_width, img_height))
        resized_frame = image.img_to_array(resized_frame) / 255
        resized_frame = np.expand_dims(resized_frame, axis=0)
        result = fire_detection_model.predict(resized_frame)
        if result[0][0] <= 0.5:
            is_fire = True
            predict = 'fire ' + str(100 - round(result[0][0] * 100, 3)) + '%'
        else:
            is_fire = False
            predict = 'not fire '
        cv2.putText(frame, predict, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 255), 4, cv2.LINE_AA)
        # Serialize frame
        data = pickle.dumps(frame)
        # Send message length first
        message_size = struct.pack("L", len(data))
        # First byte is boolean with detection result - for now for testing always True
        is_fire = struct.pack("?", is_fire)
        # Then data
        clientsocket.sendall(is_fire + message_size + data)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def stream_video_without_fire_detection_signal(cap, clientsocket):
    while True:
        ret, frame = cap.read()
        # Serialize frame
        data = pickle.dumps(frame)
        # Send message length first
        message_size = struct.pack("L", len(data))
        # Then data
        clientsocket.sendall(message_size + data)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    args = parase_arguments()
    clientsocket = connect_to_server_socket(args.H, args.P)
    cap = get_video_capture(args.source_video)
    if args.fire_detection:
        stream_video_with_fire_detection_signal(cap, clientsocket)
    else:
        stream_video_without_fire_detection_signal(cap, clientsocket)
    cap.release()
    clientsocket.stop()
