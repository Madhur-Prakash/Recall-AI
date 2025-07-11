import speech_recognition as sr
import pyttsx3
import time
import threading

# Initialize the recognizer
r = sr.Recognizer()

# Function to convert text to speech with threading
def speak_text(command):
    def _speak():
        try:
            # Create a new engine instance each time
            engine = pyttsx3.init()
            
            # Optional: Set properties for better speech quality
            engine.setProperty('rate', 150)    # Speed of speech
            engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)
            
            engine.say(command)
            engine.runAndWait()
            
            # Properly stop the engine
            engine.stop()
        except Exception as e:
            print(f"TTS Error: {e}")
    
    # Run TTS in a separate thread
    thread = threading.Thread(target=_speak)
    thread.daemon = True
    thread.start()
    thread.join(timeout=10)  # Wait max 10 seconds for speech to complete

print("Say something... (say 'exit' to quit)")

# Start listening loop
while True:
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=0.5)

            print("Listening...")
            audio = r.listen(source, timeout=5, phrase_time_limit=10)

        print("Recognizing...")
        text = r.recognize_google(audio).lower()
        print(f"You said: {text}")
        
        # Speak the recognized text
        speak_text(text)

        # Exit condition
        if any(word in text for word in ["exit", "quit", "stop"]):
            print("Exiting the program.")
            speak_text("Goodbye!")
            break

        time.sleep(0.5)  # Small pause before restarting loop

    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        speak_text("Sorry, I couldn't reach the server.")

    except sr.UnknownValueError:
        print("Could not understand audio")
        speak_text("Sorry, I didn't catch that.")
    
    except sr.WaitTimeoutError:
        print("Listening timeout")
        # Don't speak for timeout, just continue listening