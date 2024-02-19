# Michael Ruocco, eye_controller.py: This class handles eye state detection and input translation
import pyautogui
import time


class EyeController:
    def __init__(self):
        self.last_eye_closed_time = None
        self.blink_start_time = None
        self.blink_duration = 0
        self.wink_threshold = 0.2
        self.double_wink_threshold = 0.5
        self.stop_gaze_tracking_flag = False
        self.click_performed = False
        self.left_cal = 0.02
        self.right_cal = 0.02
        self.wink_duration = 0
        self.wink_frame_threshold = 0

    async def wink_detection(self, landmarks):

        left_dif = landmarks[0] - landmarks[1]
        right_dif = landmarks[2] - landmarks[3]
        left_closed = left_dif < self.left_cal / 2
        right_closed = right_dif < self.right_cal / 2

        current_time = time.time()

        if self.is_wink(left_closed, right_closed):
            if self.blink_start_time is None:
                self.blink_start_time = current_time

            if self.last_eye_closed_time is not None:
                time_since_last_eye_closed = current_time - self.last_eye_closed_time
                if 0 < time_since_last_eye_closed < self.double_wink_threshold:
                    # Double wink detected
                    if left_closed:
                        self.perform_double_left_click()
                    self.last_eye_closed_time = None  # Reset last_eye_closed_time
                    self.reset_blink_timer()
                    self.click_performed = True
                    return

            # Check for single wink
            if not self.click_performed:
                if left_closed:
                    self.perform_left_click()
                elif right_closed:
                    self.perform_right_click()
                self.last_eye_closed_time = current_time
                self.click_performed = True

        else:
            if self.blink_start_time is not None:
                self.blink_duration = current_time - self.blink_start_time
                if self.blink_duration >= 3:  # If blink duration exceeds 3 seconds
                    self.stop_gaze_tracking_flag = not self.stop_gaze_tracking_flag
                self.blink_start_time = None
                self.click_performed = False

    def is_wink(self, left_closed, right_closed):
        return (left_closed or right_closed) and (not (left_closed and right_closed))
        # cur_wink = (left_closed or right_closed) and (not (left_closed and right_closed))
        # if cur_wink:
        #     if self.wink_duration > self.wink_frame_threshold:
        #         return True
        #     else:
        #         self.wink_duration += 1
        #         return False
        # else:
        #     self.wink_duration = 0
        #     return False

    def reset_blink_timer(self):
        self.blink_start_time = None
        self.blink_duration = 0

    def set_cal(self, cal):
        self.left_cal, self.right_cal = cal

    def get_blink_duration(self):
        return self.blink_duration

    def perform_left_click(self):
        pyautogui.leftClick()

    def perform_right_click(self):
        pyautogui.rightClick()

    def perform_double_left_click(self):
        pyautogui.doubleClick()
