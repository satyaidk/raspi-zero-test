import os
import subprocess
from gpiozero import Button
from signal import pause
import speech_recognition as sr
from google import genai
from gtts import gTTS

# ==================== CONFIGURATION ====================
TOUCH_SENSOR_PIN = 17
REPLY_AUDIO_FILE = "ai_reply.mp3"

# Paste your Gemini API key directly between the quotes below:
GEMINI_API_KEY = "PASTE_YOUR_GEMINI_API_KEY_HERE"
# =======================================================

# Initialize Touch Sensor, Speech Recognizer, and Gemini Client
sensor = Button(TOUCH_SENSOR_PIN, pull_up=False)
recognizer = sr.Recognizer()

# Passing the API key directly into the client initialization
ai_client = genai.Client(api_key=GEMINI_API_KEY)

def speak_text(text_to_speak):
    """Converts text to speech and plays it through the I2S speaker."""
    try:
        print(f"AI Said: {text_to_speak}")
        
        # Generate the MP3 file using Google TTS
        tts = gTTS(text=text_to_speak, lang='en', slow=False)
        tts.save(REPLY_AUDIO_FILE)
        
        # Play the MP3 using mpg321
        subprocess.run(["mpg321", "-q", REPLY_AUDIO_FILE], check=True)
        
        # Clean up the temporary audio file after playing
        if os.path.exists(REPLY_AUDIO_FILE):
            os.remove(REPLY_AUDIO_FILE)
            
    except Exception as e:
        print(f"Error during Text-to-Speech playback: {e}")

def touched():
    print("\n[Touch detected!] Listening...")
    
    with sr.Microphone() as source:
        try:
            # Calibrate for room noise quickly
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            print("Processing your speech...")
            
            # 1. Speech to Text
            user_text = recognizer.recognize_google(audio_data)
            print(f"You said: {user_text}")
            
            # 2. Send to Gemini AI
            print("Asking Gemini...")
            response = ai_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_text,
                config={'system_instruction': "You are a voice assistant running on a small speaker device. Keep your answers brief, friendly, direct, and under 3 sentences."}
            )
            
            ai_reply = response.text
            
            # 3. Text to Speech (Play via MAX98357A)
            speak_text(ai_reply)
            
        except sr.WaitTimeoutError:
            print("[Timeout] Didn't hear anything.")
        except sr.UnknownValueError:
            print("[Error] Could not understand the audio.")
            speak_text("Sorry, I didn't quite catch that.")
        except sr.RequestError:
            print("[Error] Speech service down.")
            speak_text("I'm having trouble reaching the network.")
        except Exception as e:
            print(f"Unexpected error: {e}")

def released():
    print("Ready for next interaction.")

# Link the touch sensor to the assistant pipeline
sensor.when_pressed = touched
sensor.when_released = released

print("==================================================")
print("Smart AI Assistant Online & Ready! (Internal Key)")
print("Touch the sensor, wait for 'Listening...', and speak.")
print("==================================================")
pause()
