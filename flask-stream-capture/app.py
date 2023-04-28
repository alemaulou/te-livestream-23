from flask import Flask, request, render_template, Response
import pigpio
from datetime import datetime
import cv2
import os
from rpi_camera import RPiCamera

app = Flask(__name__)

# Set servo pin as a constant variable (may change depending on your pin)
SERVO_PIN = 17

# Importing pigpio library for smoother servo performance
# Before running, make sure to start with $ sudo pigpiod,
# or read this doc: https://gpiozero.readthedocs.io/en/stable/remote_gpio.html
pi = pigpio.pi() 

# Initialize the current frame
current_frame = 0

@app.route('/')
def index():
    # Display a message in the console when the index route is accessed
    print("Welcome")
    return render_template("index.html")

# A generator function that yields the frames captured by the camera
def gen(camera):
    # Set the current_frame variable to global
    global current_frame
    while True:
        # Capture the current frame and convert it to bytes
        current_frame = camera.get_frame() 
        frame_to_stream =  current_frame.tobytes() 

        # Set the content type of each frame to jpeg and yield the frame data in bytes
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_to_stream + b'\r\n')

@app.route('/slider', methods=['POST','GET'])
def slider():
    # Display a message in the console when the slider route is accessed
    print("Slider moved!")
    data = request.data
    # Decode the incoming data (which is in bytes)
    data = data.decode("utf-8") 
    
    # Set the pulse width to the incoming slider value
    pi.set_servo_pulsewidth(SERVO_PIN, int(data)) 
    
    return data

@app.route('/capture', methods=['POST', 'GET'])
def capture():
    data = request.data
    
    # Get the current date and time and format it for use in the file name
    now = datetime.now()
    date_time = now.strftime("%m-%d-%Y-%H:%M:%S")
    file_name = date_time + ".jpg"

    # Decode the current frame
    jpeg = cv2.imdecode(current_frame, cv2.IMREAD_COLOR)

    # Set the full path to store the captured image
    full_path = os.path.join(app.root_path, 'captured_pics', file_name)
    
    # Save the image to the full path
    cv2.imwrite(full_path , jpeg)
    
    # Return the full path (which does nothing yet, but could be used to display the captured image)
    return full_path

@app.route('/stream')
def stream():
    # Initialize the camera and set the feed as a response
    feed = Response(gen(RPiCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

    return feed

if __name__ == '__main__':
    # Run the app on the specified host and port and enable debugging
    app.run(host='0.0.0.0', port=5001, debug=True)