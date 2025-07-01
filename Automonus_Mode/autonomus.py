import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit
from time import sleep
from Sensor import sensor_for_auto_mode

kit=ServoKit(channels=16)

servo = 15
angle = 0
angle1 = 0  # Starting angle (can be adjusted as needed)

in1 = 24
in2 = 23
en = 25
in3 = 17
in4 = 27
en1 = 22

GPIO.setmode(GPIO.BCM)

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

p.start(65)
p1.start(65)

'''
frontsensor=sensor_for_auto_mode.front_sensor()
frontsensor1=sensor_for_auto_mode.front_sensor_1()
rightsensor=sensor_for_auto_mode.Right_sensor()
leftsensor=sensor_for_auto_mode.Left_sensor()
backsensor=sensor_for_auto_mode.backward_sensor()
backsensor1=sensor_for_auto_mode.backward_sensor_1()'''

def forward():
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)

def backward():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    
def stop():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)

def right_servo_move():
    for i in range(9):
        angle1 = angle1 + 10
        kit.servo[8].angle=angle1
        kit.servo[7].angle=angle1
        if sensor_for_auto_mode.front_sensor() > 60 and sensor_for_auto_mode.front_sensor_1() > 60 :
            right_side_angle = angle1
            kit.servo[8].angle=90
            kit.servo[7].angle=90
            right_side = 'unblock'
            break
        elif i == 8 and sensor_for_auto_mode.front_sensor() <= 60 and sensor_for_auto_mode.front_sensor_1() <= 60 :
            right_side_angle = angle1
            kit.servo[8].angle=90
            kit.servo[7].angle=90
            right_side = 'block'
            break
    return right_side_angle , right_side
        
def left_servo_move():
    angle1 = 90
    for i in range(9):
        angle1 = angle1 + 10
        kit.servo[8].angle=angle1
        kit.servo[7].angle=angle1
        if sensor_for_auto_mode.front_sensor() > 60 and sensor_for_auto_mode.front_sensor_1() > 60 :
            left_side_angle = angle1
            left_side = 'unblock'
            kit.servo[8].angle=90
            kit.servo[7].angle=90
            break
        elif i == 8 and sensor_for_auto_mode.front_sensor() <= 60 and sensor_for_auto_mode.front_sensor_1() <= 60 :
            left_side_angle = angle1
            kit.servo[8].angle=90
            kit.servo[7].angle=90
            left_side = 'block'
            break
    return left_side_angle , left_side

def obstracle_avoidence(rightsensor_val , leftsensor_val , right_side_angle , right_side , left_side_angle , left_side):
    if rightsensor_val == 1 and leftsensor_val == 1:
        if sensor_for_auto_mode.Right_sensor() > sensor_for_auto_mode.Left_sensor():
            if right_side != 'block':
                kit.servo[8].angle=right_side_angle
                kit.servo[7].angle=right_side_angle
                kit.servo[15].angle=(right_side_angle/2)
            elif left_side != 'block':
                kit.servo[8].angle=left_side_angle
                kit.servo[7].angle=left_side_angle
                kit.servo[15].angle=(left_side_angle/2)
        else:
            if left_side != 'block':
                kit.servo[8].angle=left_side_angle
                kit.servo[7].angle=left_side_angle
                kit.servo[15].angle=(left_side_angle/2)
            elif right_side != 'block':
                kit.servo[8].angle=right_side_angle
                kit.servo[7].angle=right_side_angle
                kit.servo[15].angle=(right_side_angle/2)
    elif rightsensor_val == 1:
        if right_side != 'block':
                kit.servo[8].angle=right_side_angle
                kit.servo[7].angle=right_side_angle
                kit.servo[15].angle=(right_side_angle/2)
    elif leftsensor_val == 1:
        if left_side != 'block':
                kit.servo[8].angle=left_side_angle
                kit.servo[7].angle=left_side_angle
                kit.servo[15].angle=(left_side_angle/2)
    front_move1 = sensor_for_auto_mode.front_sensor()
    front_move = 0
    front_move_f1 = sensor_for_auto_mode.front_sensor_1()
    front_move_f = 0
    while front_move != 30 and front_move_f != 30:
        sleep (0.05)
        forward()
        front_move = front_move1 - sensor_for_auto_mode.front_sensor()
        front_move_f = front_move_f1 - sensor_for_auto_mode.front_sensor_1()
        sleep (0.05)
    stop()
    kit.servo[8].angle=90
    kit.servo[7].angle=90
    if sensor_for_auto_mode.front_sensor() != 30 and sensor_for_auto_mode.front_sensor_1() != 30:
        front_move1 = sensor_for_auto_mode.front_sensor()
        front_move = 0
        front_move_f1 = sensor_for_auto_mode.front_sensor_1()
        front_move_f = 0
        while front_move != 20 or front_move_f != 20:
            sleep (0.05)
            forward()
            front_move = front_move1 - sensor_for_auto_mode.front_sensor()
            front_move_f = front_move_f1 - sensor_for_auto_mode.front_sensor_1()
            sleep (0.05)
        stop()
    kit.servo[8].angle = 90
    kit.servo[7].angle = 90    
    kit.servo[15].angle = 70

def check_distance():
    if sensor_for_auto_mode.front_sensor_1() < 30 or sensor_for_auto_mode.front_sensor() < 30 :
        front_move1 = sensor_for_auto_mode.front_sensor()
        front_move = 0
        front_move_f1 = sensor_for_auto_mode.front_sensor_1()
        front_move_f = 0
        while front_move != 30 or front_move_f != 30:
            sleep (0.05)
            if sensor_for_auto_mode.backward_sensor() > 30 and sensor_for_auto_mode.backward_sensor_1() > 30 :
                backward()
            else:
                stop()
            front_move = front_move1 - sensor_for_auto_mode.front_sensor()
            front_move_f = front_move_f1 - sensor_for_auto_mode.front_sensor_1()
            sleep (0.05)
        stop()
        
value = 'start'

while value == 'start':
    value = input().lower()
    
    if sensor_for_auto_mode.front_sensor() > 30 and sensor_for_auto_mode.front_sensor_1() > 30 :
        forward()
        
    elif sensor_for_auto_mode.front_sensor() <= 30 and sensor_for_auto_mode.front_sensor_1() <= 30 :
        stop()
        check_distance()
        if sensor_for_auto_mode.Right_sensor() >= 30:
            rightsensor_val = 1
            right_side_angle , right_side = right_servo_move()
            
        elif sensor_for_auto_mode.Left_sensor() >= 30:
            leftsensor_val = 1
            left_side_angle , left_side = left_servo_move()
             
        elif sensor_for_auto_mode.Left_sensor() < 30 or sensor_for_auto_mode.Right_sensor() < 30 :
            if sensor_for_auto_mode.Left_sensor() <= 20 and sensor_for_auto_mode.Right_sensor() <= 20:
                while sensor_for_auto_mode.Left_sensor() >= 30 or sensor_for_auto_mode.Right_sensor() >=30:
                    backward()
                stop()
                if sensor_for_auto_mode.Right_sensor() >= 30:
                    rightsensor_val = 1
                    right_side_angle , right_side = right_servo_move()
                    
                elif sensor_for_auto_mode.Left_sensor() >= 30:
                    leftsensor_val = 1
                    left_side_angle , left_side = left_servo_move()
                    
            #elif leftsensor >= 30 and rightsensor >= 30:
                #trap_mode()
                #break
        
        obstracle_avoidence(rightsensor_val , leftsensor_val , right_side_angle , right_side , left_side_angle , left_side)
        rightsensor_val = 0
        leftsensor_val = 0
        continue