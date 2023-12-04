# Michael Ruocco
# This class is for eye position detection to determine when a user blinks/winks
# and translate that into a right/left click

import cv2
import dlib
import numpy as np
from math import hypot
import matplotlib.pyplot as plt
import pyautogui

# Start video capture from default camera
cap = cv2.VideoCapture(0)

# Create face detector
face_detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


# Returns midpoint between two points
def midpoint(p1, p2):
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)


# Calculates the ratio between the horizontal and vertical diameter of an eye
def calculate_ratio(left, right, top_l, top_r, bottom_l, bottom_r):
    left_point = (landmarks.part(left).x, landmarks.part(left).y)
    right_point = (landmarks.part(right).x, landmarks.part(right).y)
    center_top = midpoint(landmarks.part(top_l), landmarks.part(top_r))
    center_bottom = midpoint(landmarks.part(bottom_l), landmarks.part(bottom_r))

    # Displays lines on camera frame
    hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 1)
    ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 1)

    hor_line_length = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line_length = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))
    return hor_line_length / ver_line_length


# Temporary for display
font = cv2.FONT_HERSHEY_SIMPLEX

# Parameters for calibration
calibration_frames = 200
calibration_data = []

# Calibration loop
for i in range(calibration_frames):
    _, frame = cap.read()
    frame = cv2.resize(frame, (1280, 720))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if i < 50:
        # Both eyes open calibration
        cv2.putText(frame, "Calibrating: Both eyes open. Frame {}".format(i + 1), (50, 150), font, 1, (255, 0, 0),
                    4)
    elif 50 <= i < 100:
        # Left eye open calibration
        cv2.putText(frame, "Calibrating: Right eye open. Frame {}".format(i + 1), (50, 150), font, 1, (255, 0, 0),
                    4)
    elif 100 <= i < 150:
        # Right eye open calibration
        cv2.putText(frame, "Calibrating: Left eye open. Frame {}".format(i + 1), (50, 150), font, 1, (255, 0, 0), 4)
    else:
        # Both eyes closed calibration
        cv2.putText(frame, "Calibrating: Both eyes closed. Frame {}".format(i + 1), (50, 150), font, 1, (255, 0, 0),
                    4)

    faces = face_detector(gray)
    for face in faces:
        landmarks = shape_predictor(gray, face)

        r_ratio = calculate_ratio(36, 39, 37, 38, 41, 40)
        l_ratio = calculate_ratio(42, 45, 43, 44, 47, 46)

        # Store eye aspect ratios in the calibration data
        calibration_data.append((l_ratio, r_ratio))

    # Show camera window
    cv2.imshow("Calibration", frame)
    cv2.waitKey(1)

# Destroy the calibration window
cv2.destroyWindow("Calibration")

# Create arrays for each eye state
l_open_ratio = np.array([ratio[0] for ratio in calibration_data[:50]])  # Both eyes open
r_open_ratio = np.array([ratio[1] for ratio in calibration_data[:50]])  # Both eyes open
l_l_wink_ratio = np.array([ratio[0] for ratio in calibration_data[50:100]])  # Right eye open
r_l_wink_ratio = np.array([ratio[1] for ratio in calibration_data[50:100]])  # Right eye open
l_r_wink_ratio = np.array([ratio[0] for ratio in calibration_data[100:150]])  # Left eye open
r_r_wink_ratio = np.array([ratio[1] for ratio in calibration_data[100:150]])  # Left eye open
l_blink_ratio = np.array([ratio[0] for ratio in calibration_data[150:]])  # Both eyes closed
r_blink_ratio = np.array([ratio[1] for ratio in calibration_data[150:]])  # Both eyes closed

# Calculate average for each array
l_open_ratio_avg = np.mean(l_open_ratio)
r_open_ratio_avg = np.mean(r_open_ratio)
l_l_wink_ratio_avg = np.mean(l_l_wink_ratio)
r_l_wink_ratio_avg = np.mean(r_l_wink_ratio)
l_r_wink_ratio_avg = np.mean(l_r_wink_ratio)
r_r_wink_ratio_avg = np.mean(r_r_wink_ratio)
l_blink_ratio_avg = np.mean(l_blink_ratio)
r_blink_ratio_avg = np.mean(r_blink_ratio)

# Standard deviation for each array
l_open_ratio_std = np.std(l_open_ratio)
r_open_ratio_std = np.std(r_open_ratio)
l_l_wink_ratio_std = np.std(l_l_wink_ratio)
r_l_wink_ratio_std = np.std(r_l_wink_ratio)
l_r_wink_ratio_std = np.std(l_r_wink_ratio)
r_r_wink_ratio_std = np.std(r_r_wink_ratio)
l_blink_ratio_std = np.std(l_blink_ratio)
r_blink_ratio_std = np.std(r_blink_ratio)

# Minimum and maximum values for each array using 1.5 standard deviations
l_open_ratio_min = l_open_ratio_avg - 1.5 * l_open_ratio_std
l_open_ratio_max = l_open_ratio_avg + 1.5 * l_open_ratio_std

r_open_ratio_min = r_open_ratio_avg - 1.5 * r_open_ratio_std
r_open_ratio_max = r_open_ratio_avg + 1.5 * r_open_ratio_std

l_l_wink_ratio_min = l_l_wink_ratio_avg - 1.5 * l_l_wink_ratio_std
l_l_wink_ratio_max = l_l_wink_ratio_avg + 1.5 * l_l_wink_ratio_std

r_l_wink_ratio_min = r_l_wink_ratio_avg - 1.5 * r_l_wink_ratio_std
r_l_wink_ratio_max = r_l_wink_ratio_avg + 1.5 * r_l_wink_ratio_std

l_r_wink_ratio_min = l_r_wink_ratio_avg - 1.5 * l_r_wink_ratio_std
l_r_wink_ratio_max = l_r_wink_ratio_avg + 1.5 * l_r_wink_ratio_std

r_r_wink_ratio_min = r_r_wink_ratio_avg - 1.5 * r_r_wink_ratio_std
r_r_wink_ratio_max = r_r_wink_ratio_avg + 1.5 * r_r_wink_ratio_std

l_blink_ratio_min = l_blink_ratio_avg - 1.5 * l_blink_ratio_std
l_blink_ratio_max = l_blink_ratio_avg + 1.5 * l_blink_ratio_std

r_blink_ratio_min = r_blink_ratio_avg - 1.5 * r_blink_ratio_std
r_blink_ratio_max = r_blink_ratio_avg + 1.5 * r_blink_ratio_std

# Calculate the ratios for each state
open_ratio = l_open_ratio / r_open_ratio
l_wink_ratio = l_l_wink_ratio / r_l_wink_ratio
r_wink_ratio = l_r_wink_ratio / r_r_wink_ratio
blink_ratio = l_blink_ratio / r_blink_ratio

# Calculate the differences for each state
open_dif = abs(l_open_ratio - r_open_ratio)
l_wink_dif = abs(l_l_wink_ratio - r_l_wink_ratio)
r_wink_dif = abs(l_r_wink_ratio - r_r_wink_ratio)
blink_dif = abs(l_blink_ratio - r_blink_ratio)

wink_dif_avg = (l_wink_dif + r_wink_dif) / 2
wink_std_avg = (l_l_wink_ratio_std + r_l_wink_ratio_std + l_r_wink_ratio_std + r_r_wink_ratio_std) / 4
wink_min = np.mean(wink_dif_avg - 1 * wink_std_avg)
wink_max = np.mean(wink_dif_avg + 1 * wink_std_avg)

# Create boxplots for each category
plt.boxplot([l_open_ratio, r_open_ratio, l_l_wink_ratio, r_l_wink_ratio, l_r_wink_ratio, r_r_wink_ratio, l_blink_ratio,
             r_blink_ratio],
            labels=['Left Open', 'Right Open', 'Left Left Wink', 'Right Left Wink',
                    'Left Right Wink', 'Right Right Wink', 'Left Blink', 'Right Blink'])

# Add labels and a title
plt.xlabel('Category')
plt.ylabel('Ratio')
plt.title('Boxplots of Eye Ratios')

# Show the plot
plt.show()

# Calculate the average ratio for each state
avg_open_ratio = np.mean(open_ratio)
avg_l_wink_ratio = np.mean(l_wink_ratio)
avg_r_wink_ratio = np.mean(r_wink_ratio)
avg_blink_ratio = np.mean(blink_ratio)

# Calculate the standard deviation of the ratio for each state
std_open_ratio = np.std(open_ratio)
std_l_wink_ratio = np.std(l_wink_ratio)
std_r_wink_ratio = np.std(r_wink_ratio)
std_blink_ratio = np.std(blink_ratio)

print("Left Open Ratio Min:", l_open_ratio_min)
print("Left Open Ratio Max:", l_open_ratio_max)

print("Right Open Ratio Min:", r_open_ratio_min)
print("Right Open Ratio Max:", r_open_ratio_max)

print("Left Left Wink Ratio Min:", l_l_wink_ratio_min)
print("Left Left Wink Ratio Max:", l_l_wink_ratio_max)

print("Right Left Wink Ratio Min:", r_l_wink_ratio_min)
print("Right Left Wink Ratio Max:", r_l_wink_ratio_max)

print("Left Right Wink Ratio Min:", l_r_wink_ratio_min)
print("Left Right Wink Ratio Max:", l_r_wink_ratio_max)

print("Right Right Wink Ratio Min:", r_r_wink_ratio_min)
print("Right Right Wink Ratio Max:", r_r_wink_ratio_max)

print("Left Blink Ratio Min:", l_blink_ratio_min)
print("Left Blink Ratio Max:", l_blink_ratio_max)

print("Right Blink Ratio Min:", r_blink_ratio_min)
print("Right Blink Ratio Max:", r_blink_ratio_max)

# Set dynamic thresholds based on the average ratios
blink_threshold = 0
wink_threshold = 0
detected = False
current_state = 0
frame_count = 0
open_count = 0
l_wink_count = 0
r_wink_count = 0
blink_count = 0
disp_text = ""

# Main loop for detection
while True:
    _, frame = cap.read()
    frame = cv2.resize(frame, (1280, 720))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_detector(gray)
    for face in faces:
        landmarks = shape_predictor(gray, face)

        # Calculate eye ratios
        r_ratio = calculate_ratio(36, 39, 37, 38, 41, 40)
        l_ratio = calculate_ratio(42, 45, 43, 44, 47, 46)

        ratio_dif = abs(l_ratio - r_ratio)

        # Detect open, if not blink detect which eye winked
        if not detected:
            if (l_ratio <= l_open_ratio_max) and (r_ratio <= r_open_ratio_max):
                # cv2.putText(frame, "OPEN", (50, 150), font, 3, (0, 255, 255), 4)
                open_count += 1
                current_state = 0
            elif wink_min <= ratio_dif <= wink_max:
                if (l_l_wink_ratio_min <= l_ratio <= l_l_wink_ratio_max) and (
                        r_l_wink_ratio_min <= r_ratio <= r_l_wink_ratio_max) and l_ratio > r_ratio:
                    l_wink_count += 1
                    current_state = 1
                    # cv2.putText(frame, "LEFT WINK", (50, 150), font, 3, (0, 255, 0), 4)
                    detected = True
                    # pyautogui.leftClick()
                elif (l_r_wink_ratio_min <= l_ratio <= l_r_wink_ratio_max) and (
                        r_r_wink_ratio_min <= r_ratio <= r_r_wink_ratio_max) and r_ratio > l_ratio:
                    r_wink_count += 1
                    current_state = 2
                    # cv2.putText(frame, "RIGHT WINK", (50, 150), font, 3, (0, 0, 255), 4)
                    detected = True
                    # pyautogui.rightClick()
            elif (l_blink_ratio_min <= l_ratio <= l_blink_ratio_max) and (
                    r_blink_ratio_min <= r_ratio <= r_blink_ratio_max):
                blink_count += 1
                current_state = 3
                # cv2.putText(frame, "BLINK", (50, 150), font, 3, (255, 0, 0), 4)
                detected = True

    max_state = max(blink_count, l_wink_count, r_wink_count, open_count)

    frame_count += 1
    if frame_count >= 5:
        detected = False
        frame_count = 0

        if blink_count == max_state and current_state == 3:
            disp_text = "BLINK"
        elif l_wink_count == max_state and current_state == 1:
            disp_text = "LEFT"
        elif r_wink_count == max_state and current_state == 2:
            disp_text = "RIGHT"
        elif open_count == max_state and current_state == 0:
            disp_text = "OPEN"

        open_count = 0
        l_wink_count = 0
        r_wink_count = 0
        blink_count = 0
    cv2.putText(frame, disp_text, (50, 150), font, 3, (0, 255, 0), 4)
    # Temporary to show camera on screen
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()
