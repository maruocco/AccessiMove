# Jack Duggan, head_controller.py: This class handles the head gesture recognition and input translation
import os
import mediapipe as mp
import pyautogui


def calculate_distance(a, b):
    return a - b


class HeadController:
    def __init__(self):
        self.flg = True

    async def detect_head_tilt(self, landmarks):
        left_shoulder = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].x
        right_shoulder = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].x
        left_mouth = landmarks[mp.solutions.pose.PoseLandmark.MOUTH_LEFT.value].x
        right_mouth = landmarks[mp.solutions.pose.PoseLandmark.MOUTH_RIGHT.value].x

        nose = landmarks[mp.solutions.pose.PoseLandmark.NOSE.value].y
        shoulder = (landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].y +
                    landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].y) / 2

        left_distance = calculate_distance(left_shoulder, left_mouth)
        right_distance = calculate_distance(right_mouth, right_shoulder)
        nod_distance = calculate_distance(shoulder, nose)

        if left_distance < 0.10:
            pyautogui.press('right')
        elif right_distance < 0.10:
            pyautogui.press('left')
        elif nod_distance > 0.35:
            # pyautogui.press('up')  # Uncomment if you want to enable up tilt action
            if self.flg:
                os.system("C:\\PROGRA~1\\COMMON~1\\MICROS~1\\ink\\tabtip.exe")
                self.flg = False
        elif nod_distance < 0.15:
            pyautogui.press('down')
