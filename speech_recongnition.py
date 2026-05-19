import subprocess
from gpiozero import Button
from signal import pause
import speech_recognition as sr

# Configuration
TOUCH_SENSOR_PIN = 17

# Initialize the touch sensor
sensor = Button(TOUCH_SENSOR_PIN, pull_up=False)

# Initialize the Speech Recognizer instance
recognizer = sr.Recognizer()

def touched():
    print("\n[Touch detected!] Opening microphone... Speak now.")
    
    # Use the Pi's default I2S microphone input
    with sr.Microphone() as source:
        try:
            # Adjusts the recognizer sensitivity for background noise
            print("Adjusting for ambient noise... (1 second)")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            print("Listening...")
            # phrase_time_limit stops recording if you pause for too long
            audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Processing speech...")
            
            # Convert speech to text using Google's free web API
            # Note: This requires an active internet connection on your Pi
            text = recognizer.recognize_google(audio_data)
            print(f"\n[Result] Recognized Text: {text}")
            
        except sr.WaitTimeoutError:
            print("[Timeout] No speech was detected.")
        except sr.UnknownValueError:
            print("[Error] Could not understand the audio.")
        except sr.RequestError as e:
            print(f"[Error] Could not request results from the service; {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

def released():
    print("Target released! Ready for next touch.")

# Link the actions to the sensor events
sensor.when_pressed = touched
sensor.when_released = released

print("System Ready. Touch the sensor to start Speech-to-Text...")
print("Press Ctrl+C to exit.")
pause()
