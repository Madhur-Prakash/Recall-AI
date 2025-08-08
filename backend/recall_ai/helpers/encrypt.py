import glob
import os
from cryptography.fernet import Fernet
from recall_ai.helpers.utils import setup_logging

logger = setup_logging()

def encrypt_file_data(text_dir: str = "images_taken/"):
    text_files = glob.glob(os.path.join(text_dir, "*.txt"))
    logger.info(f"✅ Found {len(text_files)} img -> text files")

    if not text_files:
        return {"error": "No text files found to process."}
    
    files = []
    # os.chdir("ransomware")
    for file in os.listdir(text_dir):
        if (file == "encrypt.py" or file == "thekey.key" or file == "decrypt.py"): # Skip these files
            continue
        if os.path.isfile(file):
            files.append(file)

    key = Fernet.generate_key()

    with open("thekey.key", "wb") as thekey:
        thekey.write(key) # Save the key to a file

    for file in files:
        with open(file, "rb") as thefile:
            contents = thefile.read() # Read the contents of the file
        encrypted_contents = Fernet(key).encrypt(contents) # Encrypt the contents
        with open(file, "wb") as thefile:
            thefile.write(encrypted_contents) # Write the encrypted contents back to the file