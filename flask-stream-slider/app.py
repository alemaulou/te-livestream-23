from flask import Flask, request, render_template, Response
import pigpio
from rpi_camera import RPiCamera

app = Flask(__name__)

SERVO_PIN = 17
pi = pigpio.pi()
angle = 500
 

@app.route('/')
def index():
    print("welcome")
    return render_template("index.html")


#the generator, a special type of function that yields, instead of returns.
def gen(camera):
   
    while True:
        frame = camera.get_frame()       
        # Each frame is set as a jpg content type. Frame data is in bytes.
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/slider', methods=['POST','GET'])
def slider():
    print("slider moved!")
    data = request.data
    data = data.decode("utf-8") #data comes in bytes; need to decode.

    pi.set_servo_pulsewidth(SERVO_PIN, int(data))

    
    return data


@app.route('/stream')
def stream():

    feed = Response(gen(RPiCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

    print(type(feed))
    return feed

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True )