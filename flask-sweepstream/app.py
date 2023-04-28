from flask import Flask, render_template, Response
import pigpio
from rpi_camera import RPiCamera

app = Flask(__name__)

SERVO_PIN = 17
pi = pigpio.pi()
angle = 500
sweep = 1

@app.route('/')
def index():
    return render_template("index.html")


#the generator, a special type of function that yields, instead of returns.
def gen(camera):
    global angle, sweep
    while True:
        frame = camera.get_frame()
        pi.set_servo_pulsewidth(SERVO_PIN, angle)
        angle =  angle + sweep 
        if angle == 2000:
            sweep = -1
        if angle == 501:
            sweep = 1
        
        

        # Each frame is set as a jpg content type. Frame data is in bytes.
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/stream')
def stream():

    feed = Response(gen(RPiCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

    print(type(feed))
    return feed

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True )