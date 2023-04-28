from flask import Flask, request, render_template, Response
import pigpio
from datetime import datetime
import cv2
import os
from rpi_camera import RPiCamera

app = Flask(__name__)

SERVO_PIN = 17
"""
The pigpio library offers smoother servo performance:
$ sudo apt-get install pigpio python-pigpio python3-pigpio

NOTE:Before running, make sure to start with $ sudo pigpiod,
 or read this doc: https://gpiozero.readthedocs.io/en/stable/remote_gpio.html
     
"""
pi = pigpio.pi() 
current_frame = 0

@app.route('/')
def index():
    print("welcome")
    return render_template("index.html")


#the generator, a special type of function that yields, instead of returns.
def gen(camera):
    global current_frame
    while True:
        
        """
         In this version we keep a separte jpg frame to capture before
         we convert to bytes.
        """
        current_frame = camera.get_frame() 
        frame_to_stream =  current_frame.tobytes() 

        # Each frame is set as a jpg content type. Frame data is in bytes.
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_to_stream + b'\r\n')

@app.route('/slider', methods=['POST','GET'])
def slider():
    print("slider moved!")
    data = request.data
    data = data.decode("utf-8") #data comes in bytes; need to decode.

    #set the pulse width to the incoming slider value
    pi.set_servo_pulsewidth(SERVO_PIN, int(data)) 
    
    return data

@app.route('/capture', methods=['POST', 'GET'])
def capture():
    data = request.data
    
    now = datetime.now()
    date_time = now.strftime("%m-%d-%Y-%H:%M:%S")
    file_name = date_time + ".jpg"

    #image was encoded with cv2.encode, so we need to decode it. 
    jpeg = cv2.imdecode(current_frame, cv2.IMREAD_COLOR)

    #We will store pics in /captured_pics, found in the root folder.
    full_path = os.path.join(app.root_path, 'captured_pics', file_name)
    
    #Save the image
    cv2.imwrite(full_path , jpeg)
    
    #return full_path does nothing yet, but it could be use to display pic.
 
    return full_path

@app.route('/stream')
def stream():

    feed = Response(gen(RPiCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

    return feed

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True )