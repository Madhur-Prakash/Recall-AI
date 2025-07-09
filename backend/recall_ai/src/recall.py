import numpy as np
import cv2
import pyautogui
import pytesseract
import traceback
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.models import demo
from config.database import mongo_client
from helpers.utils import create_new_log, setup_logging

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

image1 = pyautogui.screenshot("image1.png")


# OCR
def ocr_image(image_path):
    try:
        # Read the image using OpenCV
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Image not found or unable to read.")

        # Convert the image to RGB (pytesseract expects RGB format)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Use pytesseract to do OCR on the image
        text = pytesseract.image_to_string(image_rgb).strip()

        full_text = " ".join(text.split())
        return full_text

        
    except Exception as e:
        # create_new_log(f"Error in OCR: {str(e)}")
        traceback.print_exc()
        return None
    
ans = ocr_image("image.png")
if ans:
    print("OCR Result:", ans)
else:
    print("OCR failed to extract text.")


