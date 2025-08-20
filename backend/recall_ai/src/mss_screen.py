import json
import sys
import os
import platform
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from screeninfo import get_monitors
import cv2
import numpy as np
import time
from datetime import datetime
from mss import mss
from recall_ai.helpers.screen_shot import ocr_image
from helpers.utils import setup_logging
from helpers.encrypt import encrypt_file_data
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv() 

# Configuration
THRESHOLD_PIXELS = 100000  # Number of changed pixels to trigger detection
FRAME_DELAY = 4  # Delay between frames in seconds
display_dict = {}
monitor_dict = {}
capture_regions = []
previous_frames = {}
logging = setup_logging()
output_dir = 'images_taken'
os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists


def get_monitor_info_windows():
    """Get detailed monitor information on Windows using WMI"""
    try:
        import wmi
        
        # detecting display devices using WMI
        obj = wmi.WMI().Win32_PnPEntity(ConfigManagerErrorCode=0)
        displays = [x for x in obj if 'DISPLAY' in str(x)]

        # Get monitor EDID-based info from WmiMonitorID (hardware-accurate)
        wmi_monitors = wmi.WMI(namespace='wmi').WmiMonitorID()

        # Decode WmiMonitorID fields
        def decode_edid_field(field):
            if field is None:
                return ""
            return ''.join(chr(c) for c in field if c != 0)

        # Prepare readable monitor names from EDID
        edid_names = []
        for monitor in wmi_monitors:
            # Try to get a meaningful name in order of preference
            user_friendly_name = decode_edid_field(monitor.UserFriendlyName)
            manufacturer = decode_edid_field(monitor.ManufacturerName)
            product_code = decode_edid_field(monitor.ProductCodeID)
            serial = decode_edid_field(monitor.SerialNumberID)
            
            # Determine the best display name
            if user_friendly_name:
                display_name = user_friendly_name
            elif manufacturer and product_code:
                # For integrated displays, create a meaningful name
                if manufacturer == "BOE" and product_code:
                    display_name = f"BOE {product_code} (Integrated Display)"
                else:
                    display_name = f"{manufacturer} {product_code}"
            elif manufacturer:
                display_name = f"{manufacturer} Display"
            elif product_code:
                display_name = f"Display {product_code}"
            else:
                display_name = "Unknown Display"
            
            # Handle serial number (avoid showing just "0")
            if serial and serial != "0":
                serial_display = serial
            else:
                serial_display = "N/A"
            
            edid_names.append({
                "name": display_name,
                "manufacturer": manufacturer or "Unknown",
                "serial": serial_display,
                "product_code": product_code or "Unknown"
            })
        
        return edid_names
    except ImportError:
        logging.warning("WMI not available - using basic monitor detection")
        return []

def get_monitor_info_linux():
    """Get basic monitor information on Linux (fallback)"""
    try:
        # Try to get display info from xrandr if available
        import subprocess
        result = subprocess.run(['xrandr', '--listmonitors'], 
                              capture_output=True, text=True, check=True)
        monitors_info = []
        lines = result.stdout.strip().split('\n')[1:]  # Skip header
        
        for i, line in enumerate(lines):
            if line.strip():
                # Parse xrandr output (basic parsing)
                parts = line.split()
                if len(parts) >= 4:
                    name = parts[-1] if parts[-1] != 'primary' else f"Monitor-{i+1}"
                    monitors_info.append({
                        "name": name,
                        "manufacturer": "Unknown",
                        "serial": "N/A",
                        "product_code": "Unknown"
                    })
        return monitors_info
    except (ImportError, subprocess.CalledProcessError, FileNotFoundError):
        logging.warning("xrandr not available - using generic monitor names")
        return []

def setup_monitors():
    """Setup monitor information based on the current platform"""
    # Get screen resolutions and positions
    monitors = get_monitors()
    
    # Get detailed monitor info based on platform
    current_platform = platform.system().lower()
    
    if current_platform == "windows":
        detailed_info = get_monitor_info_windows()
    else:
        detailed_info = get_monitor_info_linux()
    
    # Process monitors
    for i, monitor in enumerate(monitors):
        # Match detailed info if available
        if i < len(detailed_info):
            info = detailed_info[i]
            name = info["name"]
            manufacturer = info["manufacturer"]
            serial = info["serial"]
        else:
            # Fallback for when detailed info is not available
            name = f"Monitor-{i+1}"
            manufacturer = "Unknown"
            serial = "N/A"
        
        # Store monitor info in a dictionary
        monitor_dict[i] = {
            "name": name,
            "manufacturer": manufacturer,
            "serial": serial,
            "width": monitor.width,
            "height": monitor.height,
            "resolution": f"{monitor.width}x{monitor.height}",
            "x": monitor.x,
            "y": monitor.y,
            "is_primary": monitor.is_primary,
            "platform": current_platform
        }
        
        # Create capture region for each monitor and store in list
        capture_region = {
            "top": monitor.y,
            "left": monitor.x,
            "width": monitor.width,
            "height": monitor.height
        }
        capture_regions.append(capture_region)
        logging.info(f"Gathered monitor info for {name}: {monitor.width}x{monitor.height}")
        
        # Initialize previous frame for each monitor
        previous_frames[i] = None

# Setup monitors
setup_monitors()

sct = mss()

print(f"Starting screen change detector on {platform.system()}... Press Ctrl+C to stop.")
print(f"Detected {len(monitor_dict)} monitor(s)")

try:
    while True:
        # Loop through all monitors
        for i, monitor in enumerate(get_monitors()):
            # Capture screenshot for current monitor
            screenshot = sct.grab(capture_regions[i])
            frame = np.array(screenshot)

            # Convert to grayscale for comparison
            gray_current = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if previous_frames[i] is not None:
                diff = cv2.absdiff(previous_frames[i], gray_current)
                _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

                changed_pixels = np.sum(thresh) // 255

                if changed_pixels > THRESHOLD_PIXELS:
                    logging.info(f"Screen change detected! ({changed_pixels} pixels changed) in monitor {i + 1} - {monitor_dict[i]['name']}")
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Screen change detected! ({changed_pixels} pixels changed) in monitor {i + 1} - {monitor_dict[i]['name']}")
                    img_name = f"image_{i + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    file_path = os.path.join(output_dir, img_name)

                    # Use MSS to capture the actual image
                    screenshot = sct.grab(capture_regions[i])
                    img = np.array(screenshot)
                    cv2.imwrite(file_path, cv2.cvtColor(img, cv2.COLOR_BGRA2BGR))  # Convert from BGRA to BGR

                    print(f"Screenshot saved as {img_name}")
                    logging.info(f"Screenshot saved as {img_name} for monitor {i + 1} - {monitor_dict[i]['name']}")
                    res = ocr_image(file_path)
                    if res:
                        # Save OCR result to a text file
                        text_file_path = os.path.join(output_dir, f"ocr_{i + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
                        with open(text_file_path, 'w', encoding='utf-8') as f:
                            f.write(res)
                        success = encrypt_file_data()
                        if not success:
                            logging.error(f"❌ Encryption failed for {text_file_path}.")
                        else:
                            logging.info(f"🔐 Encryption successful for {text_file_path}.")

                        if (os.path.exists(file_path)):
                            os.remove(file_path) # delete the image after OCR
                        logging.info(f"✅ OCR text result for image of {monitor_dict[i]['name']} is extracted successfully.")
                    else:
                        logging.error(f"❌ OCR failed to extract text for image of {monitor_dict[i]['name']}.")
                        print("OCR failed to extract text.")

            previous_frames[i] = gray_current.copy()
        
        time.sleep(FRAME_DELAY)

except KeyboardInterrupt:
    logging.info("Screen change detection stopped by user.")
    print("\nStopped by user.")