from gpiozero import Button
from signal import pause

sensor = Button(17, pull_up=False)

def touched():
    print("Touch detected!")

def released():
    print("Target released!")

sensor.when_pressed = touched
sensor.when_released = released

print("Touch the sensor now...")
pause()
