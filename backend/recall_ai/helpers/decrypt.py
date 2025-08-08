import glob
import os
from cryptography.fernet import Fernet
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from recall_ai.helpers.utils import setup_logging

logger = setup_logging()
KEY_FILE = "thekey.key"

def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            key = f.read()
            logger.info("🔑 Loaded existing encryption key.")
        return key
    logger.warning("🔑 Encryption key not found.")
    return None

def decrypt_file_data(text_dir: str = "images_taken/"):
    key = load_key()
    files_to_decrypt = glob.glob(os.path.join(text_dir, "*.enc"))
    logger.info(f"✅ Found {len(files_to_decrypt)} files to decrypt.")

    if not files_to_decrypt:
        return {"message": "No files to decrypt."}

    for filepath in files_to_decrypt:
        try:
            with open(filepath, "rb") as file:
                contents = file.read()
            decrypted_content = Fernet(key).decrypt(contents)
            dec_filepath = filepath[:-4] + ".txt"  # Remove .enc and add .txt
            with open(dec_filepath, "wb") as file:
                file.write(decrypted_content)
            os.remove(filepath)
            logger.info(f"🔓 Decrypted file: {filepath} -> {dec_filepath}")
        except Exception as e:
            logger.error(f"Failed to decrypt {filepath}: {e}")

    return {"message": "Decryption completed successfully."}