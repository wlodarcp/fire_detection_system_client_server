import cv2


def get_video_capture(source = None):
    if source is None:
        return cv2.VideoCapture(0)
    else:
        return cv2.VideoCapture(source)