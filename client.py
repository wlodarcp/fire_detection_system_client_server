# -*- coding: utf-8 -*-
import pickle
import socket
import struct

import cv2

from ArgumentParaser import parase_arguments
from VideoSourceProvider import get_video_capture


def connect_to_server_socket(HOST, port):
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((HOST, port))
    return clientsocket


def stream_video_with_fire_detection_signal(cap, clientsocket):
    while True:
        ret, frame = cap.read()
        # Serialize frame
        data = pickle.dumps(frame)
        # Send message length first
        message_size = struct.pack("L", len(data))
        # First byte is boolean with detection result - for now for testing always True
        is_fire = struct.pack("?", True)
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
