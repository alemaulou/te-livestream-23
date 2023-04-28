# Import necessary libraries
import cv2
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import numpy as np

# Define a class for Raspberry Pi camera
class RPiCamera(object):

    def __init__(self):
        # Start the video stream from the Raspberry Pi camera
        self.stream = PiVideoStream().start()
        # Wait for 2 seconds to warm up the camera
        time.sleep(2.0)

    def __del__(self):
        # Stop the video stream when the object is destroyed
        self.stream.stop()

    def get_frame(self):
        # Read a frame from the video stream
        frame = self.stream.read()

        # Encode the frame in JPEG format
        result, jpeg = cv2.imencode('.jpg', frame)

        # Return the frame in bytes format
        return jpeg.tobytes()