import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

def setup_output(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

def turn_on(pin):
    GPIO.output(pin, GPIO.LOW)

def turn_off(pin):
    GPIO.output(pin, GPIO.HIGH)
