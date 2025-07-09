import cv2
import numpy as np
import pyautogui # or mss

previous_frame = None

while True:
    # Capture current screen frame
    screenshot = pyautogui.screenshot()
    frame_np = np.array(screenshot)
    current_frame = cv2.cvtColor(frame_np, cv2.COLOR_RGB2BGR)

    if previous_frame is not None:
        gray_previous = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
        gray_current = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

        diff = cv2.absdiff(gray_previous, gray_current)
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

        change_pixels = np.sum(thresh)

        if change_pixels > 1000:  # Adjust this threshold as needed
            print("Screen change detected!")

    previous_frame = current_frame.copy()

    # Optional: Display the difference for debugging
    # cv2.imshow("Difference", thresh)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

# cv2.destroyAllWindows()