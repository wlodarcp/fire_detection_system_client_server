import pickle
import socket
import struct

from threading import Thread
import cv2

from datetime import date

current_date = date.today()

cameras = [[1, 8098], [2, 8010]]
HOST = 'localhost'

def create_sockets(cameras):
    sockets = {}
    for camera in cameras:
        camera_id = camera[0]
        sockets[camera_id] = create_socket_for_camera(camera_id, camera[1])
    print(sockets)
    return sockets        
        
def create_socket_for_camera(camera_id, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created for camera {' + str(camera_id) + '} on port {' + str(port) + '}')
    s.bind((HOST, port))
    print('Socket bind complete')
    s.listen(10)
    print('Socket now listening')
    return s


def listen_on_socket(socket, camera_id):
    while True:
        conn, addr = socket.accept()     # Establish connection with client.
        on_new_client(conn, camera_id)
    
def on_new_client(clientsocket, camera_id):
    data = b''
    payload_size = struct.calcsize("L")
    print("Camera " + str(camera_id) + " CONNECTED to the server")
    vid_cod = cv2.VideoWriter_fourcc(*'XVID')
    path = str('videos/' + current_date.strftime("%b-%d-%Y") + '/cam_' + str(camera_id) + '.mp4')
    output = None
    while True:
        try:
            while len(data) < payload_size:
                received = clientsocket.recv(4096)
                if not received: raise Exception()
                data += received

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0] ### CHANGED

            # Retrieve all data based on message size
            while len(data) < msg_size:
                data += clientsocket.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]
                

        # Extract frame
            frame = pickle.loads(frame_data)
            if output is None:
                output = cv2.VideoWriter(str('first_cam_' + str(camera_id) + '.avi'), vid_cod, 20.0, (frame.shape[1],frame.shape[0]))
        # Display
            cv2.imshow(str('frame_for_camera-' + str(camera_id)), frame)
            cv2.waitKey(1)
            output.write(frame)
        except:
            print("Camera " + str(camera_id) + " DISCONNECTED")
            output.release()
            cv2.destroyWindow(str('frame_for_camera-' + str(camera_id)))
            break

if __name__ == "__main__":
    sockets = create_sockets(cameras)
    for camera_id in sockets:
        Thread(target = listen_on_socket,args = (sockets[camera_id], camera_id,)).start()
    
