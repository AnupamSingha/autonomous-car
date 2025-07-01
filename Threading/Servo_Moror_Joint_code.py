import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#from all_sensor import Right_sensor, Left_sensor, backward_sensor
import all_sensor

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
temp1=1

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

p.start(25)
p1.start(25)


while True:
	command = input("Enter command (\n l=servo-left,\n " "r=servo-right,\n " "c=servo-center,\n " "s=motor-stop,\n " "f=motor-forward,\n " "b=motor-backward,\n " "sl=motor-slow,\n " "m=motor-medium,,\n " "mh=motor-medium-high,\n " "h=motor-high \n): ").lower()
	
	if command == 'l':
		
		GPIO.output(in1,GPIO.LOW)
		GPIO.output(in2,GPIO.LOW)
		GPIO.output(in3,GPIO.LOW)
		GPIO.output(in4,GPIO.LOW)
		
		if angle <= 160 and angle1 <= 160 and angle2 <= 160:
			angle =(angle + step)
			angle1 =(angle1 + step1)
			angle2 = (angle2 - step)
			kit.servo[8].angle = angle
			kit.servo[15].angle = angle1
			kit.servo[7].angle = angle2
		else:
			print("angles are at max limit (160°)")

	elif command == 'r':
		
		GPIO.output(in1,GPIO.LOW)
		GPIO.output(in2,GPIO.LOW)
		GPIO.output(in3,GPIO.LOW)
		GPIO.output(in4,GPIO.LOW)
		
		if angle >= 20 and angle1 >= 20 and angle2 >= 20:
			angle = (angle - step)
			angle1 = (angle1 - step1)
			angle2 = (angle2 + step)
			kit.servo[8].angle = angle
			kit.servo[15].angle = angle1
			kit.servo[7].angle = angle2
		else:
			print("angles are at min limit (20°)")


	elif command == 'c':
		
		GPIO.output(in1,GPIO.LOW)
		GPIO.output(in2,GPIO.LOW)
		GPIO.output(in3,GPIO.LOW)
		GPIO.output(in4,GPIO.LOW)
		
		angle=90
		angle1=70
		angle2=90
		kit.servo[8].angle=angle
		kit.servo[15].angle=angle1
		kit.servo[7].angle=angle2

	elif command == 's':
        	print("stop")
        	GPIO.output(in1,GPIO.LOW)
        	GPIO.output(in2,GPIO.LOW)
        	GPIO.output(in3,GPIO.LOW)
        	GPIO.output(in4,GPIO.LOW)
        	command ='z'

	elif command == 'f':
		print("forward")
		running = True
		print("Enter s for stop the car")
		while running:
			frontsensor=all_sensor.front_sensor()
			rightsensor=all_sensor.Right_sensor()
			leftsensor=all_sensor.Left_sensor()
		
			#print(frontsensor)
			#print(rightsensor)
			#print(leftsensor)
		
			if (frontsensor + rightsensor + leftsensor) == 0:
				print("unblock")
				GPIO.output(in1,GPIO.HIGH)
				GPIO.output(in2,GPIO.LOW)
				GPIO.output(in3,GPIO.HIGH)
				GPIO.output(in4,GPIO.LOW)
				temp1=1
				command='z'
			elif (frontsensor + rightsensor + leftsensor) == 1:
				print("block")
				GPIO.output(in1,GPIO.LOW)
				GPIO.output(in2,GPIO.LOW)
				GPIO.output(in3,GPIO.LOW)
				GPIO.output(in4,GPIO.LOW)
				temp1=1
				command='z'
			#elif input("Press 'q' to quit: ").lower() == 'q':
				#running = False

	elif command == 'b':
		print("backward")
		while True:
			leftsensor=all_sensor.Right_sensor()
			rightsensor=all_sensor.Left_sensor()
			backwardsensor=all_sensor.backward_sensor()
		
			print(backwardsensor)
			print(rightsensor)
			print(leftsensor)
		
			#if backwardsensor == 0 or rightsensor == 0 or leftsensor == 0:
			if (backwardsensor + rightsensor + leftsensor) == 0:
				GPIO.output(in1,GPIO.LOW)
				GPIO.output(in2,GPIO.HIGH)
				GPIO.output(in3,GPIO.LOW)
				GPIO.output(in4,GPIO.HIGH)
				temp1=0
				command='z'
			#elif frontsensor == 1 or rightsensor == 1 or leftsensor == 1:
			elif (backwardsensor + rightsensor + leftsensor) == 1:
				GPIO.output(in1,GPIO.LOW)
				GPIO.output(in2,GPIO.LOW)
				GPIO.output(in3,GPIO.LOW)
				GPIO.output(in4,GPIO.LOW)
				temp1=1
				command='z'

	elif command == 'sl':
        	print("low")
        	p.ChangeDutyCycle(25)
        	p1.ChangeDutyCycle(25)
        	command='z'

	elif command == 'm':
        	print("medium")
        	p.ChangeDutyCycle(50)
        	p1.ChangeDutyCycle(50)
        	command='z'
		
	elif command == 'mh':
        	print("medium-high")
        	p.ChangeDutyCycle(75)
        	p1.ChangeDutyCycle(75)
        	command='z'

	elif command == 'h':
        	print("high")
        	p.ChangeDutyCycle(100)
        	p1.ChangeDutyCycle(100)
        	command='z'
		
	elif command == 'sn':
		leftsensor=all_sensor.Right_sensor()
		rightsensor=all_sensor.Left_sensor()
		backwardsensor=all_sensor.backward_sensor()
		
		print(backwardsensor)
		print(rightsensor)
		print(leftsensor)
		
	else:
		print("-------Invalid command---------")
		continue

#print("Enter command (\n l=servo-left,\n " "r=servo-right,\n " "c=servo-center,\n " "s=motor-stop,\n " "f=motor-forward,\n " "b=motor-backward,\n " "l=motor-low,\n " "m=motor-medium,\n " "h=motor-high \n): ")
