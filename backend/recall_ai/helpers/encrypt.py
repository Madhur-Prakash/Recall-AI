import glob
import os
from cryptography.fernet import Fernet
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from recall_ai.helpers.utils import setup_logging
from dotenv import load_dotenv

logger = setup_logging()
load_dotenv()
KEY_FILE = "thekey.key"
IMAGE_DIR = os.getenv("IMAGES_DIR")


def load_or_create_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            key = f.read()
            logger.info("🔑 Loaded existing encryption key.")
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        logger.info("🔑 Generated and saved new encryption key.")
    return key


def encrypt_file_data(text_dir: str = IMAGE_DIR):
    key = load_or_create_key()

    # Only encrypt files without .enc extension
    files_to_encrypt = glob.glob(os.path.join(text_dir, "*.txt"))
    files_to_encrypt = [f for f in files_to_encrypt if not f.endswith(".enc")]

    logger.info(f"✅ Found {len(files_to_encrypt)} text files to encrypt.")

    if not files_to_encrypt:
        return {"message": "No new files to encrypt."}

    for filepath in files_to_encrypt:
        try:
            with open(filepath, "rb") as file:
                contents = file.read()
            encrypted_content = Fernet(key).encrypt(contents)
            # Write encrypted data to a new file with .enc suffix
            enc_filepath = filepath.replace(".txt", ".enc")
            with open(enc_filepath, "wb") as file:
                file.write(encrypted_content)
            # Optionally, delete the original file after encryption
            os.remove(filepath)
            logger.info(f"🔒 Encrypted file: {filepath} -> {enc_filepath}")
        except Exception as e:
            logger.error(f"Failed to encrypt {filepath}: {e}")

    return {"message": "Encryption completed successfully."}