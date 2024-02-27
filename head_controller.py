# Jack Duggan, Michael Ruocco, head_controller.py: This class handles the head gesture recognition and input translation
import mediapipe as mp
import pyautogui
import win32api
import win32con
from settings import Settings


def calculate_distance(a, b):
    return a - b


class HeadController:
    def __init__(self):
        self.settings = Settings()
        self.flg = True
        self.screen_width, self.screen_height = pyautogui.size()
        self.corner = (int(self.screen_width / 2), int(self.screen_height / 2), int(self.screen_width / 2) - 1,
                       int(self.screen_height / 2) - 1)
        self.prev_x, self.prev_y = pyautogui.position()
        self.up_thresh = 1
        self.down_thresh = 0
        self.left_thresh = 0.10
        self.right_thresh = 0.10
        self.nod_distance = 0
        self.left_distance = 0
        self.right_distance = 0
        self.press_performed = False

    async def detect_head_tilt(self, landmarks, head_track_flag):
        left_shoulder = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].x
        right_shoulder = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].x
        left_mouth = landmarks[mp.solutions.pose.PoseLandmark.MOUTH_LEFT.value].x
        right_mouth = landmarks[mp.solutions.pose.PoseLandmark.MOUTH_RIGHT.value].x

        nose = landmarks[mp.solutions.pose.PoseLandmark.NOSE.value].y
        shoulder = (landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].y +
                    landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].y) / 2

        self.left_distance = calculate_distance(left_shoulder, left_mouth)
        self.right_distance = calculate_distance(right_mouth, right_shoulder)
        self.nod_distance = calculate_distance(shoulder, nose)
        # if self.nod_distance > self.up_thresh or self.nod_distance < self.down_thresh + .1:
            # print(self.nod_distance)
        if self.left_distance < self.left_thresh and not head_track_flag:
            self.press_arrow_key(0x27)
        elif self.right_distance < self.right_thresh and not head_track_flag:
            self.press_arrow_key(0x25)
        elif self.nod_distance > self.up_thresh:
            self
            if head_track_flag:
                try:
                    open_x, open_y = pyautogui.locateCenterOnScreen('Images/keyboard_img.png', grayscale=True, region=(
                        self.corner), confidence=0.6)
                    self.click_move(open_x, open_y)
                except:
                    pass
            else:
                self.press_arrow_key(0x26)
        elif self.nod_distance < self.down_thresh:
            if head_track_flag:
                try:
                    guide_x, guide_y = pyautogui.locateCenterOnScreen('Images/x_out_guide.png', grayscale=True, region=(
                        self.corner), confidence=0.6)
                    guide_y -= int(self.screen_height / 20)
                    x_dist = self.screen_width - guide_x - 1
                    y_dist = self.screen_height - guide_y - 1
                    close_x, close_y = pyautogui.locateCenterOnScreen('Images/x_out.png', grayscale=True, region=(
                        guide_x, guide_y, x_dist, y_dist), confidence=0.6)
                    self.click_move(close_x, close_y)
                except:
                    pass
            else:
                self.press_arrow_key(0x28)
        else:
            self.press_performed = False

    def click_move(self, x, y):
        self.prev_x, self.prev_y = win32api.GetCursorPos()
        pyautogui.click(x, y)
        win32api.SetCursorPos((self.prev_x, self.prev_y))

    def press_arrow_key(self, key):
        if not self.press_performed:
            win32api.keybd_event(key, 0, 0, 0)
            win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)
        self.press_performed = True

    def get_nod_distance(self, landmarks, head_track_flag):
        left_shoulder = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].x
        right_shoulder = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].x
        left_mouth = landmarks[mp.solutions.pose.PoseLandmark.MOUTH_LEFT.value].x
        right_mouth = landmarks[mp.solutions.pose.PoseLandmark.MOUTH_RIGHT.value].x

        nose = landmarks[mp.solutions.pose.PoseLandmark.NOSE.value].y
        shoulder = (landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].y +
                    landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].y) / 2

        self.left_distance = calculate_distance(left_shoulder, left_mouth)
        self.right_distance = calculate_distance(right_mouth, right_shoulder)
        self.nod_distance = calculate_distance(shoulder, nose)
        return self.nod_distance

    def set_nod_cal(self, up_distance, down_distance):
        self.up_thresh = up_distance
        self.down_thresh = down_distance
        print(f"Thresh: {self.up_thresh, self.down_thresh}")
