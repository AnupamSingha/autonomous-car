from flask import Flask, redirect, url_for, request,render_template,Response
import RPi.GPIO as GPIO     # Import Library to access GPIO PIN
import cv2
import time

from Sensor import all_sensor

from adafruit_servokit import ServoKit

import threading
move_thread = None  # Thread object
stop_event = threading.Event()  # Event to stop the thread

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

kit=ServoKit(channels=16)

servo = 15
angle = 90  # Starting angle (can be adjusted as needed)
angle1 = 80
angle2 = 90
step = 20  # Step size for angle change
step1 = 10


in1 = 24
in2 = 23
en = 25
in3 = 17
in4 = 27
en1 = 22

GPIO.setup(16, GPIO.OUT)

GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)

GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en1,GPIO.OUT)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)

GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)

p=GPIO.PWM(en,1000)
p1=GPIO.PWM(en1,1000)

p.start(50)
p1.start(50)

video_capture = cv2.VideoCapture(0)

Url_Address = "192.168.28.162"
app = Flask(__name__)


def generate_frames():
    while True:
        result, output = video_capture.read()
        cv2.imshow('frame', output)
        ret, buffer = cv2.imencode('.jpg', output)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
@app.route('/video_feed')
def video_feed():
    print ("Error: unable to fecth data")
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


#moving_forward = False
#moving_backward = False
#servo_left_moving = False
#servo_right_moving = False

def move_forward():
    """ Continuous forward movement in a separate thread """
    print("Moving forward...")
    stop_event.clear()
        
    while not stop_event.is_set():
        frontsensor=all_sensor.front_sensor()
        rightsensor=all_sensor.Right_sensor()
        leftsensor=all_sensor.Left_sensor()
        
        if frontsensor == 1 and (rightsensor+leftsensor) == 1 :
                
                GPIO.output(16, GPIO.HIGH)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in4,GPIO.LOW)
                
        elif frontsensor == 0 and (rightsensor+leftsensor) == 1 :
                
                GPIO.output(16, GPIO.HIGH)
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in3,GPIO.HIGH)
                GPIO.output(in4,GPIO.LOW)
        
        elif frontsensor == 0 and (rightsensor+leftsensor) == 0 :
                
                GPIO.output(16, GPIO.LOW)
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in3,GPIO.HIGH)
                GPIO.output(in4,GPIO.LOW)
                
        elif frontsensor == 1 and (rightsensor+leftsensor) == 0 :
                
                GPIO.output(16, GPIO.HIGH)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in4,GPIO.LOW)
                
                
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

def move_backward():
    """ Continuous forward movement in a separate thread """
    print("Moving Backward...")
    stop_event.clear()
    
    while not stop_event.is_set():
        backwardsensor=all_sensor.backward_sensor()
        leftsensor=all_sensor.Right_sensor()
        rightsensor=all_sensor.Left_sensor()
        
        if backwardsensor == 0 and (rightsensor+leftsensor) == 1 :
                
                GPIO.output(16, GPIO.HIGH)
                
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in4,GPIO.HIGH)
        
        elif backwardsensor == 0 and (rightsensor+leftsensor) == 0 :
                
                GPIO.output(16, GPIO.LOW)
                
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in4,GPIO.HIGH)
                
        elif backwardsensor == 1 and (rightsensor+leftsensor) == 0 :
                
                GPIO.output(16, GPIO.HIGH)
                
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in4,GPIO.LOW)
                
        elif backwardsensor == 1 and (rightsensor+leftsensor) == 1 :
                
                GPIO.output(16, GPIO.HIGH)
                
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in4,GPIO.LOW)

# Smooth PWM movement function
def smooth_pwm_move(start, end, servo, steps=5, delay=0.05):
    """Smoothly moves servo from start to end using PWM ramping"""
    step_size = (end - start) / steps
    for i in range(steps + 1):
        current_angle = start + (i * step_size)
        kit.servo[servo].angle = current_angle
        sleep(delay)
                
def moving_servo_right_way():
    """ Continuous forward movement in a separate thread """
    global servo_right_moving
    while servo_right_moving:
        rightsensor=all_sensor.Right_sensor()
        
        if rightsensor == 1 :
                
                GPIO.output(16, GPIO.HIGH)
                
        elif rightsensor == 0 :
                
                GPIO.output(16, GPIO.LOW)
                
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in4,GPIO.LOW)
		
                if angle <= 160 and angle1 <= 160 and angle2 <= 160:
                        new_angle = (angle + step)
                        new_angle1 = (angle1 + step1)
                        new_angle2 = (angle2 - step)

                        smooth_pwm_move(angle, new_angle, 8)
                        smooth_pwm_move(angle1, new_angle1, 15)
                        smooth_pwm_move(angle2, new_angle2, 7)

                        angle = new_angle
                        angle1 = new_angle1
                        angle2 = new_angle2
                        
                        
def moving_servo_left_way():
    """ Continuous forward movement in a separate thread """
    global servo_left_moving
    while servo_left_moving:
        leftsensor=all_sensor.Left_sensor()
        
        if leftsensor == 1 :
                
                GPIO.output(16, GPIO.HIGH)
                
        elif leftsensor == 0 :
                
                GPIO.output(16, GPIO.LOW)
                
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in4,GPIO.LOW)
		
                if angle >= 20 and angle1 >= 20 and angle2 >= 20:
                        new_angle = (angle - step)
                        new_angle1 = (angle1 - step1)
                        new_angle2 = (angle2 + step)
                        
                        smooth_pwm_move(angle, new_angle, 8)
                        smooth_pwm_move(angle1, new_angle1, 15)
                        smooth_pwm_move(angle2, new_angle2, 7)

                        angle = new_angle
                        angle1 = new_angle1
                        angle2 = new_angle2

@app.route('/Forward',methods = ['POST', 'GET'])
def Forward():
   try:
        print ("Forward")
        global move_thread

        # Check if the thread is already running, if so stop it before restarting
        if move_thread and move_thread.is_alive():
                stop_movement()

        # Start new thread for movement
        move_thread = threading.Thread(target=move_forward, daemon=True)
        move_thread.start()

        return render_template("OmniRobor 4.0.html", HTML_address=Url_Address)
        
   except:
      print ("Error: unable to fecth data")

@app.route('/Backward',methods = ['POST', 'GET'])
def Backward():
   try:
        print ("backward")  
        global move_thread

        # Check if the thread is already running, if so stop it before restarting
        if move_thread and move_thread.is_alive():
                stop_movement()

        # Start new thread for movement
        move_thread = threading.Thread(target=move_backward, daemon=True)
        move_thread.start()

        return render_template("OmniRobor 4.0.html", HTML_address=Url_Address)
   except:
      print ("Error: unable to fecth data")

@app.route('/left',methods = ['POST', 'GET'])
def left():
   try:
        print ("servo_left_turning")
        global servo_left_moving
        if not servo_left_moving:
                servo_left_moving = True
                return render_template("OmniRobor 4.0.html",HTML_address=Url_Address)
   except:
      print ("Error: unable to fecth data")

@app.route('/right',methods = ['POST', 'GET'])
def right():
   try:
        print ("servo_right_turning")
        global servo_right_moving
        if not servo_right_moving:
                servo_right_moving = True
                return render_template("OmniRobor 4.0.html",HTML_address=Url_Address) 
   except:
      print ("Error: unable to fecth data")

@app.route('/stop',methods = ['POST', 'GET'])
def stop():
   try:
        stop_movement()
        return render_template("OmniRobor 4.0.html", HTML_address=Url_Address)  
   except:
      print ("Error: unable to fecth data")

@app.route('/')
def login():
   return render_template("OmniRobor 4.0.html",HTML_address=Url_Address)      

      
if __name__ == '__main__':
   app.run(Url_Address,8080,threaded=True)



