import json
import cv2 # used for image processing
from kafka import KafkaProducer
import pytesseract # used for OCR
import traceback
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers.utils import setup_logging

logging = setup_logging()
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# OCR
def ocr_image(image_path):
    try:
        # Read the image using OpenCV
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Image not found or unable to read.")
        logging.info(f"Image loaded successfully from {image_path}")
        # Convert the image to RGB (pytesseract expects RGB format)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Use pytesseract to do OCR on the image
        text = pytesseract.image_to_string(image_rgb).strip()

        full_text = " ".join(text.split())
        logging.info("OCR text extracted")  # Log first 100 characters for brevity

        #  sending OCR result to Kafka
        producer.send('ocr_results', {'image_path': image_path, 'text': full_text})
        producer.flush()  # Ensure the message is sent immediately
        return full_text

        
    except Exception as e:
        formatted_error = traceback.format_exc()
        logging.error(f"Error in OCR: {formatted_error}")
        return None
