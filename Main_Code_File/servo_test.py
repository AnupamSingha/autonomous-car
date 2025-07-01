import RPi.GPIO as gpio
from adafruit_servokit import ServoKit
from time import sleep

kit=ServoKit(channels=16)

servo = 15
angle = 90  # Starting angle (can be adjusted as needed)
step = 20  # Step size for angle change


while True:
	command = input("Enter command (l=left, r=right, s=stop, c=center): ").lower()
	if command == 'l':
		angle = min(180, angle + step) # Ensure it doesn't exceed 180 degrees
		kit.servo[8].angle=angle
		kit.servo[15].angle=angle
	elif command == 'r':
		angle = max(0, angle - step)  # Ecnsure it doesn't go below 0 degrees
		kit.servo[8].angle=angle
		kit.servo[15].angle=angle
	elif command == 's':
		print("Servo stopped")
		continue
	elif command == 'c':
		angle=90
		angle1=70
		kit.servo[8].angle=angle
		kit.servo[15].angle=angle1
	else:
		print("Invalid command. Use 'l', 'r', 's', or 'c'")
		continue

