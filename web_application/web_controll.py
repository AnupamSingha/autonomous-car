from flask import Flask, redirect, url_for, request, render_template, Response
import RPi.GPIO as GPIO
import cv2
import time
from Sensor import all_sensor
from adafruit_servokit import ServoKit
import threading

# Initialize Flask app
app = Flask(__name__)

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Servo and Motor Config
kit = ServoKit(channels=16)

# Servo angles
servo = 15
angle = 90  
step = 20

# Motor pins
in1, in2, en = 24, 23, 25
in3, in4, en1 = 17, 27, 22

# GPIO setup
GPIO.setup(16, GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(en1, GPIO.OUT)

GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)

p = GPIO.PWM(en, 1000)
p1 = GPIO.PWM(en1, 1000)
p.start(50)
p1.start(50)

# Video streaming
video_capture = cv2.VideoCapture(0)

# URL settings
Url_Address = "192.168.143.162"

# Movement control variables
move_thread = None
stop_event = threading.Event()

### 🎥 **Video Streaming Function**
def generate_frames():
    while True:
        result, frame = video_capture.read()
        if not result:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


### 🔥 **Motor Movement Functions**
def move_forward():
    """ Continuous forward movement in a separate thread """
    print("Moving forward...")
    stop_event.clear()

    while not stop_event.is_set():
        frontsensor = all_sensor.front_sensor()
        rightsensor = all_sensor.Right_sensor()
        leftsensor = all_sensor.Left_sensor()

        if frontsensor == 1 and (rightsensor + leftsensor) == 1:
            GPIO.output(16, GPIO.HIGH)
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.LOW)
            GPIO.output(in3, GPIO.LOW)
            GPIO.output(in4, GPIO.LOW)

        elif frontsensor == 0 and (rightsensor + leftsensor) == 1:
            GPIO.output(16, GPIO.HIGH)
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
            GPIO.output(in3, GPIO.HIGH)
            GPIO.output(in4, GPIO.LOW)

        elif frontsensor == 0 and (rightsensor + leftsensor) == 0:
            GPIO.output(16, GPIO.LOW)
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
            GPIO.output(in3, GPIO.HIGH)
            GPIO.output(in4, GPIO.LOW)

        elif frontsensor == 1 and (rightsensor + leftsensor) == 0:
            GPIO.output(16, GPIO.HIGH)
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.LOW)
            GPIO.output(in3, GPIO.LOW)
            GPIO.output(in4, GPIO.LOW)

        time.sleep(0.1)


### 🛑 **Stop Movement**
def stop_movement():
    """ Stop all motor movements """
    global move_thread

    print("Stopping movement...")
    stop_event.set()

    # Ensure the thread stops cleanly
    if move_thread and move_thread.is_alive():
        move_thread.join()

    # Reset GPIO states
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    time.sleep(0.1)


### 🌐 **Flask Routes**
@app.route('/Forward', methods=['POST', 'GET'])
def forward():
    global move_thread

    # Check if the thread is already running, if so stop it before restarting
    if move_thread and move_thread.is_alive():
        stop_movement()

    # Start new thread for movement
    move_thread = threading.Thread(target=move_forward, daemon=True)
    move_thread.start()

    return render_template("OmniRobor 4.0.html", HTML_address=Url_Address)


@app.route('/stop', methods=['POST', 'GET'])
def stop():
    stop_movement()
    return render_template("OmniRobor 4.0.html", HTML_address=Url_Address)


@app.route('/')
def login():
    return render_template("OmniRobor 4.0.html", HTML_address=Url_Address)


### 🚦 **Run the Flask App**
if __name__ == '__main__':
    app.run(Url_Address, port=8080, threaded=True)
