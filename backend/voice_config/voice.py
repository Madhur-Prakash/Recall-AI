import torch
import sounddevice as sd
import numpy as np
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import pyttsx3
import time
import requests
import threading
from recall_ai.helpers.utils import setup_logging
from recall_ai.src.recall import get_chat_response

# Initialize the TTS engine (removed global engine to avoid threading issues)
# Each thread will create its own engine instance

# Load Whisper Large V3 model (best quality)
print("Loading Whisper Large V3 model (best quality)...")
print("Note: This model is ~3GB and may take time to download on first run")

model_name = "openai/whisper-large-v3"  # Best Whisper model
processor = WhisperProcessor.from_pretrained(model_name)
model = WhisperForConditionalGeneration.from_pretrained(
    model_name,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32  # Use float16 for GPU efficiency
)

# Alternative models by quality (uncomment to use):
# model_name = "openai/whisper-large-v2"  # Previous best version
# model_name = "openai/whisper-medium"     # Good balance of speed/quality  
# model_name = "openai/whisper-small"      # Faster, still good quality
# model_name = "openai/whisper-base"       # Basic quality
# model_name = "openai/whisper-tiny.en"    # Fastest, English-only

# Move to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()
logger = setup_logging()

# Audio recording parameters
SAMPLE_RATE = 16000
DURATION = 10  # seconds
CHANNELS = 1

def record_audio(duration=5):
    """Record audio from microphone"""
    print(f"Recording for {duration} seconds...")
    logger.info(f"Recording audio for {duration} seconds...")
    audio_data = sd.rec(int(duration * SAMPLE_RATE), 
                       samplerate=SAMPLE_RATE, 
                       channels=CHANNELS, 
                       dtype=np.float32)
    sd.wait()  # Wait until recording is finished
    return audio_data.flatten()

def transcribe_audio_direct(audio_data):
    """Transcribe audio using direct model inference"""
    try:
        logger.info("Transcribing audio directly with Whisper model...")
        # Process audio
        input_features = processor(
            audio_data, 
            sampling_rate=SAMPLE_RATE, 
            return_tensors="pt"
        ).input_features
        
        # Move to device
        input_features = input_features.to(device)
        
        # Generate transcription with proper settings
        with torch.no_grad():
            predicted_ids = model.generate(
                input_features,
                language="en",  # Force English to avoid language detection warnings
                task="transcribe",  # Explicit task setting
                forced_decoder_ids=None  # Remove deprecated parameter
            )
        
        # Decode the transcription
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        logger.info(f"Transcription result: {transcription}")
        
        return transcription.strip().lower()
        
    except Exception as e:
        print(f"Transcription error: {e}")
        return None

def speak_text(command):
    """Convert text to speech with threading"""
    def _speak():
        try:
            logger.info(f"Speaking command: {command}")
            # Create a new engine instance for thread safety
            local_engine = pyttsx3.init()
            local_engine.setProperty('rate', 150)
            local_engine.setProperty('volume', 0.9)
            
            local_engine.say(command)
            local_engine.runAndWait()
            local_engine.stop()
            
        except Exception as e:
            print(f"TTS Error: {e}")
    
    thread = threading.Thread(target=_speak)
    thread.daemon = True
    thread.start()
    thread.join(timeout=10)

async def process_with_server(text):
    """
    Alternative: Call the chat function directly if it's in the same application
    """
    try:
        logger.info(f"Processing text with server: {text}")
        response = await get_chat_response(text)
        logger.info(f"Server response: {response}")
        return response
    except Exception as e:
        logger.error(f"Local function error: {e}")
        return "Sorry, I couldn't process your request."


# def main():
#     print("Voice Assistant with Direct Whisper Model")
#     print("Say something... (say 'exit' to quit)")
    
#     while True:
#         try:
#             # Record audio
#             audio_data = record_audio(DURATION)
            
#             # Check if audio has sufficient volume
#             if np.max(np.abs(audio_data)) < 0.01:
#                 print("No speech detected, continuing...")
#                 continue
            
#             print("Transcribing...")
#             text = transcribe_audio_direct(audio_data)
            
#             if text:
#                 print(f"You said: {text}")
                
#                 # Process with your server
#                 server_response = process_with_server(text)
                
#                 if server_response:
#                     print(f"Server response: {server_response}")
#                     speak_text(server_response)
#                 else:
#                     speak_text("Sorry, I couldn't process your request.")
                
#                 # Exit condition
#                 if any(word in text for word in ["exit", "quit", "stop"]):
#                     print("Exiting the program.")
#                     speak_text("Goodbye!")
#                     break
#             else:
#                 print("Could not transcribe audio")
#                 speak_text("Sorry, I didn't catch that.")
                
#             time.sleep(0.5)
            
#         except KeyboardInterrupt:
#             print("\nExiting...")
#             speak_text("Goodbye!")
#             break
#         except Exception as e:
#             print(f"Error: {e}")
#             speak_text("Sorry, something went wrong.")

# if __name__ == "__main__":
#     main()