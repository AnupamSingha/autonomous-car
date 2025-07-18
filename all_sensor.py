import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Assign unique trigger and echo pins for each sensor
#backward
TRIG = 29   #green
ECHO = 31	#yellow

#front
TRIG1 = 29   #green
ECHO1 = 33	#yellow

#left
TRIG2 = 29   #green
ECHO2 = 35	#yellow

#rignt
TRIG3 = 29   #green
ECHO3 = 37	#yellow

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

try:
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

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nProgram terminated.")
    GPIO.cleanup()
