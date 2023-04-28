from flask import Flask, request, render_template, Response
import pigpio
from rpi_camera import RPiCamera

app = Flask(__name__)

SERVO_PIN = 2 # define the GPIO pin number to which the servo motor is connected
pi = pigpio.pi() # create an instance of the pigpio library
angle = 500 # initialize the angle variable'

# note: angle is initialized to 500. This is because angle is being 
# used to set the initial position of the servo motor connected to SERVO_PIN. 
# The value of 500 is a pulse width modulation (PWM) value that represents 
# the initial position of the servo motor in microseconds. The value of 500 in 
# PWM means that the servo motor is positioned at 0 degrees (the minimum angle of the 
# servo motor). PWM signal of 500 microseconds corresponds to the minimum position 
# of the servo motor, 2000 max.

# define the index route that returns the rendered template
@app.route('/')
def index():
    print("welcome")
    return render_template("index.html")

# define a generator function named 'gen' that yields frames from the RPiCamera
def gen(camera):
    while True:
        global angle
        frame = camera.get_frame()
        # set the servo pulsewidth to the angle value
        pi.set_servo_pulsewidth(SERVO_PIN, angle)
        # generate the next angle value
        angle += 1
        if angle > 2500:
            angle = 500
        # yield the frame as a multipart jpeg
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# define the slider route to receive data from the slider on the frontend
@app.route('/slider', methods=['POST','GET'])
def slider():
    print("slider moved!")
    data = request.data
    # decode the data from bytes to string
    data = data.decode("utf-8")
    print(int(data))
    # set the servo pulsewidth to the value of the slider 
    pi.set_servo_pulsewidth(SERVO_PIN, int(data))
    # return the data received from the slider
    return data

# define the video stream route
@app.route('/stream')
def stream():
    # generate the video feed from the camera using the gen function
    feed = Response(gen(RPiCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')
    # print the type of the feed
    print(type(feed))
    # return the feed
    return feed

# start the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True )