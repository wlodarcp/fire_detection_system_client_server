import argparse

def parase_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', default='localhost', type=str, help="Server HOST to connect")
    parser.add_argument('-P', default=8080, type=int, help="Server port to connect")
    parser.add_argument('--source_video', type=str, help="Path for video source - if not set video from camera on local machine is streamed")
    parser.add_argument('--no-fire-detection', dest='fire_detection', action='store_false', help="Disable fire detection enabled - by default True")
    parser.set_defaults(fire_detection=True)
    return parser.parse_args()
