import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Assign unique trigger and echo pins for each sensor
#front
TRIG = 5   #green
ECHO = 26	#yellow 26

#front1
TRIG_f1 = 5   #green
ECHO_f1 = 11	#yellow 26

#backward
TRIG1 = 5   #green
ECHO1 = 19	#yellow 13

#backward1
TRIG1_b1 = 5   #green
ECHO1_b1 = 9	#yellow 13

#right
TRIG2 = 5   #green
ECHO2 = 6	#yellow 19

#left
TRIG3 = 5   #green
ECHO3 = 13	#yellow 6

# Setup GPIO pins
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(TRIG_f1, GPIO.OUT)
GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(TRIG1_b1, GPIO.OUT)
GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(TRIG3, GPIO.OUT)

GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(ECHO_f1, GPIO.IN)
GPIO.setup(ECHO1, GPIO.IN)
GPIO.setup(ECHO1_b1, GPIO.IN)
GPIO.setup(ECHO2, GPIO.IN)
GPIO.setup(ECHO3, GPIO.IN)

# Initialize trigger pins to LOW
GPIO.output(TRIG, False)
GPIO.output(TRIG_f1, False)
GPIO.output(TRIG1, False)
GPIO.output(TRIG1_b1, False)
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
    if distance == 'none':
        distance = 100
        return distance
    else:
        return distance
    
def front_sensor_1():

    distance_f1 = get_distance(TRIG_f1, ECHO_f1)
    if distance_f1 == 'none':
        distance_f1 = 100
        return distance_f1
    else:
        return distance_f1

def backward_sensor():

    distance1 = get_distance(TRIG1, ECHO1)
    if distance1 == 'none':
        distance1 = 100
        return distance1
    else:
        return distance1
    
def backward_sensor_1():

    distance_b1 = get_distance(TRIG1_b1, ECHO1_b1)
    if distance_b1 == 'none':
        distance_b1 = 100
        return distance_b1
    else:
        return distance_b1

def Right_sensor():

    distance2 = get_distance(TRIG2, ECHO2)
    if distance2 == 'none':
        distance2 = 100
        return distance2
    else:
        return distance2

def Left_sensor():

    distance3 = get_distance(TRIG3, ECHO3)
    if distance3 == 'none':
        distance3 = 100
        return distance3
    else:
        return distance3        
        
if __name__ == "__main__":
    while True:
        front_sensor()
        front_sensor_1()
        backward_sensor()
        backward_sensor_1()
        Right_sensor()
        Left_sensor()
