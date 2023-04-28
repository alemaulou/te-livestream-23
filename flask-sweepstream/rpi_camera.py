import cv2
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import numpy as np



class RPiCamera(object):

    # Define a constructor that initializes the PiVideoStream 
    # object and waits for 2 seconds for the camera to warm up.
    def __init__(self):
        self.stream = PiVideoStream().start()
        time.sleep(2.0)

    # Define a destructor that stops the PiVideoStream 
    # object when the RPiCamera object is deleted.
    def __del__(self):
        self.stream.stop()


    # Define a method called get_frame() that returns a single frame 
    # from the camera as a JPEG-encoded byte string. 
    # The frame is obtained by calling the read() method of the 
    # PiVideoStream object, and then encoding it as a JPEG using 
    # OpenCV's imencode() function. The resulting JPEG byte string 
    # is returned.
    def get_frame(self):
        frame = self.stream.read()

        result, jpeg = cv2.imencode('.jpg', frame)



        return jpeg.tobytes()