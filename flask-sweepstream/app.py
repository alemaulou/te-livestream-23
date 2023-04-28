from flask import Flask, render_template, Response
import pigpio
from rpi_camera import RPiCamera

app = Flask(__name__)

SERVO_PIN = 2
pi = pigpio.pi() # create an instance of the pigpio library
angle = 500 # initialize the angle variable'
sweep = 1

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
    return render_template("index.html")


# define a generator function named 'gen' that yields frames from the RPiCamera
def gen(camera):
    global angle, sweep
    while True:
        # get a frame from the camera
        frame = camera.get_frame()
        # set the PWM value to the servo motor
        pi.set_servo_pulsewidth(SERVO_PIN, angle)
        # increment the angle variable with a sweep variable
        angle = angle + sweep 
        # if angle reaches maximum value, change the sweep direction to negative
        if angle == 2000:
            sweep = -1
        # if angle reaches minimum value, change the sweep direction to positive
        if angle == 501:
            sweep = 1
        
        # yield the frame as a multipart jpeg response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# define a route named 'stream' that returns a multipart HTTP response with the frames from the RPiCamera
@app.route('/stream')
def stream():
    # create a Response object with the generator function that yields the frames
    feed = Response(gen(RPiCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')
   
    # print the type of the feed object
    print(type(feed))

    # return the feed object as the HTTP response
    return feed

# start the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True )