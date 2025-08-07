import cv2 # used for image processing
import pytesseract # used for OCR
import traceback
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers.utils import setup_logging
from paddleocr import PaddleOCR

# Initialize once globally to avoid reloading model every time
# ocr_model = PaddleOCR(use_angle_cls=True, lang='en')  # Use 'en' or 'en+hi' etc.
logging = setup_logging()
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

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
        return full_text

    
    except Exception as e:
        formatted_error = traceback.format_exc()
        logging.error(f"Error in OCR: {formatted_error}")
        return None


# PaddleOCR
# def ocr_image_paddle(image_path):
#     try:
#         # Read the image using OpenCV
#         image = cv2.imread(image_path)
#         if image is None:
#             raise ValueError("Image not found or unable to read.")
#         logging.info(f"Image loaded successfully from {image_path}")

#         # Run OCR using PaddleOCR
#         result = ocr_model.predict(image, cls=True)

#         # Extract text and flatten
#         text_list = [line[1][0] for line in result[0]]
#         full_text = " ".join(text_list).strip()

#         logging.info("OCR text extracted")
#         return full_text

#     except Exception as e:
#         formatted_error = traceback.format_exc()
#         logging.error(f"Error in Paddle OCR: {formatted_error}")
#         return None