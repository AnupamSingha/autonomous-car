import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Assign unique trigger and echo pins for each sensor
#front
TRIG = 5   #green
ECHO = 26	#yellow 26

#backward
TRIG1 = 5   #green
ECHO1 = 19	#yellow 13

#right
TRIG2 = 5   #green
ECHO2 = 6	#yellow 19

#left
TRIG3 = 5   #green
ECHO3 = 13	#yellow 6

# Setup GPIO pins
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(TRIG3, GPIO.OUT)

GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(ECHO1, GPIO.IN)
GPIO.setup(ECHO2, GPIO.IN)
GPIO.setup(ECHO3, GPIO.IN)

# Initialize trigger pins to LOW
GPIO.output(TRIG, False)
GPIO.output(TRIG1, False)
GPIO.output(TRIG2, False)
GPIO.output(TRIG3, False)

def get_distance(trig, echo):
    """Function to trigger sensor and measure distance"""
    # Trigger the sensor
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    # Wait for echo signal
    start_time, end_time = None, None

    # Wait for the signal to start
    timeout = time.time() + 0.1  # Add timeout to prevent infinite loop
    while GPIO.input(echo) == 0:
        start_time = time.time()
        if time.time() > timeout:
            return None  # Timeout case

    # Wait for the signal to end
    timeout = time.time() + 0.1
    while GPIO.input(echo) == 1:
        end_time = time.time()
        if time.time() > timeout:
            return None

    if start_time is None or end_time is None:
        return None  # Handle cases where pulse wasn't detected

    pulse_duration = end_time - start_time
    distance = pulse_duration * 17150
    return round(distance, 2)
    
    
def front_sensor():

    distance = get_distance(TRIG, ECHO)
    if distance is not None and distance <= 20:
        #print(f"Front Sensor: {distance} cm")
        return 1
    else:
        return 0

def backward_sensor():

    distance1 = get_distance(TRIG1, ECHO1)
    if distance1 is not None and distance1 <= 20:
        #print(f"Backward Sensor: {distance1} cm")
        return 1
    else:
        return 0

def Right_sensor():

    distance2 = get_distance(TRIG2, ECHO2)
    if distance2 is not None and distance2 <= 20:
        #print(f"Left Sensor: {distance2} cm")
        return 1
    else:
        return 0

def Left_sensor():

    distance3 = get_distance(TRIG3, ECHO3)
    if distance3 is not None and distance3 <= 20:
        #print(f"Right Sensor: {distance3} cm")
        return 1
    else:
        return 0        
        
if __name__ == "__main__":
    while True:
        front_sensor()
        backward_sensor()
        Right_sensor()
        Left_sensor()
    
'''
----------------------------------------
while True:
    # Measure distances from all sensors
    distance = get_distance(TRIG, ECHO)
    distance1 = get_distance(TRIG1, ECHO1)
    distance2 = get_distance(TRIG2, ECHO2)
    distance3 = get_distance(TRIG3, ECHO3)

        # Print distances if valid
    if distance is not None and distance <= 20:
        print(f"Backward Sensor: {distance} cm")

    if distance1 is not None and distance1 <= 20:
        print(f"Front Sensor: {distance1} cm")

    if distance2 is not None and distance2 <= 20:
        print(f"Left Sensor: {distance2} cm")

    if distance3 is not None and distance3 <= 20:
        print(f"Right Sensor: {distance3} cm")
'''
    
'''
----------------------------------------
while True:
    # Measure distances from all sensors
    distance = get_distance(TRIG, ECHO)
    distance1 = get_distance(TRIG1, ECHO1)
    distance2 = get_distance(TRIG2, ECHO2)
    distance3 = get_distance(TRIG3, ECHO3)

        # Print distances if valid
    if distance is not None and distance <= 20:
        print(f"Backward Sensor: {distance} cm")

    if distance1 is not None and distance1 <= 20:
        print(f"Front Sensor: {distance1} cm")

    if distance2 is not None and distance2 <= 20:
        print(f"Left Sensor: {distance2} cm")

    if distance3 is not None and distance3 <= 20:
        print(f"Right Sensor: {distance3} cm")
'''
