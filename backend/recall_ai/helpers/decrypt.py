import os
from cryptography.fernet import Fernet

def decrypt_file_data():
    files = []
    for file in os.listdir():
        if (file == "voldermort.py" or file == "thekey.key" or file == "decrypt.py"): # Skip the script and key file
            continue
        if os.path.isfile(file):
            files.append(file)

    with open("thekey.key", "rb") as thekey:
        key = thekey.read() # Read the key from the file


    for file in files:
        with open(file, "rb") as thefile:
            contents = thefile.read() # Read the contents of the file
        decrypted_contents = Fernet(key).decrypt(contents) # Encrypt the contents
        with open(file, "wb") as thefile:
            thefile.write(decrypted_contents) # Write the encrypted contents back to the file