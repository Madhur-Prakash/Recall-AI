import wmi
from screeninfo import get_monitors
import cv2
import numpy as np
import time
from datetime import datetime
from mss import mss
import wmi

# Configuration
THRESHOLD_PIXELS = 100000  # Number of changed pixels to trigger detection
FRAME_DELAY = 1  # Delay between frames in seconds
SHOW_DEBUG_WINDOW = False  # Set True to visualize diff frame
display_dict = {}
monitor_dict = {}


# # detecting display devices using WMI
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
    # print(f"Monitor EDID: {monitor}")
    
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
# Get screen resolutions and positions
monitors = get_monitors()

# Print monitor info
print(f"Monitors detected via screeninfo: {len(monitors)}\n")

for i, monitor in enumerate(monitors):
    # Match EDID info if available (best-effort by index)
    if i < len(edid_names):
        info = edid_names[i]
        name = info["name"] or "Unknown"
        manufacturer = info["manufacturer"] or "Unknown"
        serial = info["serial"] or "Unknown"
    else:
        name = manufacturer = serial = "Unknown"
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
        "is_primary": monitor.is_primary
    }
    
    # print(f"Monitor {i + 1} {monitor}:")
    # print(f"  Name        : {name}")
    # print(f"  Manufacturer: {manufacturer}")
    # print(f"  Serial No.  : {serial}")
    # print(f"  Resolution  : {monitor.width}x{monitor.height}")
    # print(f"  Position    : ({monitor.x}, {monitor.y})")
    # print(f"  Primary     : {monitor.is_primary}\n")

    # Define screen capture region (full screen by default)
    monitor = {"top": monitor_dict[i]["x"], "left": monitor_dict[i]["y"], "width": monitor_dict[i]["width"], "height": monitor_dict[i]["height"]}  # Change if needed
    
    # print(f"Monitor {i + 1} - {monitor_dict[i]['name']} ({monitor_dict[i]['resolution']}) at ({monitor_dict[i]['x']}, {monitor_dict[i]['y']})")
    previous_gray = None
    sct = mss()

print("Starting screen change detector using MSS... Press Ctrl+C to stop.")

try:
    while True:
        # Capture screenshot using MSS
        screenshot = sct.grab(monitor)
        frame = np.array(screenshot)

        # Convert to grayscale for comparison
        gray_current = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if previous_gray is not None:
            diff = cv2.absdiff(previous_gray, gray_current)
            _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

            changed_pixels = np.sum(thresh) // 255

            if changed_pixels > THRESHOLD_PIXELS:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Screen change detected! ({changed_pixels} pixels changed)")

            if SHOW_DEBUG_WINDOW:
                cv2.imshow("Change Detection", thresh)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        previous_gray = gray_current.copy()
        time.sleep(FRAME_DELAY)

except KeyboardInterrupt:
    print("\nStopped by user.")

finally:
    if SHOW_DEBUG_WINDOW:
        cv2.destroyAllWindows()
