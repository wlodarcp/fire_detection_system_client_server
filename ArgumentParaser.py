import argparse

def parase_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', default='localhost', type=str, help="Server HOST to connect")
    parser.add_argument('-P', default=8098, type=int, help="Server port to connect")
    parser.add_argument('--source_video', type=str, help="Path for video source - if not set video from camera on local machine is streamed")
    parser.add_argument('--fire_detection', type=bool, default=True, help="Is fire detection enabled - by default false")
    return parser.parse_args()
