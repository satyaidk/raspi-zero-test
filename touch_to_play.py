import subprocess
from gpiozero import Button
from signal import pause

# Configuration
TOUCH_SENSOR_PIN = 17
AUDIO_FILE = "fahhhhhhhhhhhhhh.mp3"

# Initialize sensor. 
# pull_up=False means it expects a HIGH (3.3V) signal when touched.
sensor = Button(TOUCH_SENSOR_PIN, pull_up=False)

def touched():
    print("\n[Touch detected!] Playing audio...")
    try:
        # Launch mpg321 to play the file through your I2S audio card
        subprocess.run(["mpg321", AUDIO_FILE], check=True)
        print("Playback finished. Ready for next touch.")
    except Exception as e:
        print(f"Error playing audio: {e}")

def released():
    print("Target released!")

# Link the actions to the sensor events
sensor.when_pressed = touched
sensor.when_released = released

print("System Ready. Touch the sensor now to play audio...")
print("Press Ctrl+C to exit.")
pause()
