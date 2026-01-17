import cv2 # used for image processing
import pytesseract # used for OCR
import traceback
import re
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers.utils import setup_logging
from dotenv import load_dotenv

logging = setup_logging()
load_dotenv()

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ---- Sensitive patterns ----
SENSITIVE_PATTERNS = {
    "PASSWORD": r"(password|passcode|pwd)\s*[:=]\s*\S+",
    "OTP": r"\b\d{4,8}\b",
    "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    "PHONE": r"\b(\+?\d{1,3}[\s-]?)?\d{10}\b",
    "CARD": r"\b(?:\d[ -]*?){13,16}\b",
    "API_KEY": r"(api[_-]?key|secret|token)\s*[:=]\s*\S+",
    "CCV_CODE": r"\b\d{3,4}\b",
    "CARD_NUMBER": r"\b(?:\d[ -]*?){13,16}\b",
    "USERNAME": r"\b(username|user id|login)\s*[:=]\s*\S+",
    "SECRET": r"(secret|private[_-]?key)\s*[:=]\s*\S+",
    "EXPIRY_DATE": r"\b(0[1-9]|1[0-2])\/?([0-9]{2}|[0-9]{4})\b",
    "IP_ADDRESS": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
    "API_TOKEN": r"(api[_-]?token|access[_-]?token)\s*[:=]\s*\S+",
    "AUTH_TOKEN": r"(auth[_-]?token|authorization)\s*[:=]\s*\S+",
    "JWT_TOKEN": r"(jwt[_-]?token|json[_-]?web[_-]?token)\s*[:=]\s*\S+"
}

REPLACEMENTS = {
    "PASSWORD": "[REDACTED_PASSWORD]",
    "OTP": "[REDACTED_OTP]",
    "EMAIL": "[REDACTED_EMAIL]",
    "PHONE": "[REDACTED_PHONE]",
    "CARD": "[REDACTED_CARD]",
    "API_KEY": "[REDACTED_SECRET]",
    "CCV_CODE": "[REDACTED_CCV]",
    "CARD_NUMBER": "[REDACTED_CARD_NUMBER]",
    "USERNAME": "[REDACTED_USERNAME]",
    "SECRET": "[REDACTED_SECRET]",
    "EXPIRY_DATE": "[REDACTED_EXPIRY_DATE]",
    "IP_ADDRESS": "[REDACTED_IP_ADDRESS]",
    "API_TOKEN": "[REDACTED_API_TOKEN]",
    "AUTH_TOKEN": "[REDACTED_AUTH_TOKEN]",
    "JWT_TOKEN": "[REDACTED_JWT_TOKEN]"
}

def sanitize_text(text: str) -> str:
    """Remove or mask sensitive information from OCR text."""
    sanitized = text

    for key, pattern in SENSITIVE_PATTERNS.items():
        sanitized = re.sub(
            pattern,
            REPLACEMENTS[key],
            sanitized,
            flags=re.IGNORECASE
        )

    return sanitized

# OCR
def ocr_image(image_path):
    try:
        # Read the image using OpenCV
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Image not found or unable to read.")

        logging.info(f"Image loaded successfully from {image_path}")

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        raw_text = pytesseract.image_to_string(image_rgb)

        # Normalize spacing
        normalized_text = " ".join(raw_text.split())

        # 🔐 Privacy filtering BEFORE storage
        sanitized_text = sanitize_text(normalized_text)

        logging.info("OCR text extracted and sanitized")
        return sanitized_text

    except Exception:
        formatted_error = traceback.format_exc()
        logging.error(f"Error in OCR: {formatted_error}")
        return None
