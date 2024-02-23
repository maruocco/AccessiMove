# Michael Ruocco, eye_controller.py: This class handles eye state detection and input translation
import win32api
import win32con
import time


def is_blink(left_closed, right_closed):
    return left_closed and right_closed


def is_wink(left_closed, right_closed):
    return (left_closed or right_closed) and (left_closed != right_closed)


def perform_left_click():
    x, y = win32api.GetCursorPos()
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def perform_right_click():
    x, y = win32api.GetCursorPos()
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)


def perform_double_left_click():
    x, y = win32api.GetCursorPos()
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


class EyeController:
    def __init__(self):
        self.blink_start_time = None
        self.blink_duration = 0
        self.stop_gaze_tracking_flag = False
        self.stop_head_tracking_flag = True
        self.click_performed = False
        self.double_click_performed = False
        self.left_cal = 0.02
        self.right_cal = 0.02
        self.left_count = 0

    async def wink_detection(self, landmarks):

        # Get distance between upper and lower eyelids
        left_dif = landmarks[0] - landmarks[1]
        right_dif = landmarks[2] - landmarks[3]
        left_closed = left_dif < self.left_cal / 1.75
        right_closed = right_dif < self.right_cal / 1.75

        current_time = time.time()

        if is_wink(left_closed, right_closed) and not self.stop_gaze_tracking_flag:

            # Check for single wink
            if not self.click_performed:
                if left_closed:
                    perform_left_click()
                elif right_closed:
                    perform_right_click()
                self.click_performed = True
                self.left_count = 0

            # If left wink is held will double-click
            elif left_closed and not self.double_click_performed:
                self.left_count += 1
                if self.left_count > 4:
                    perform_double_left_click()
                    self.double_click_performed = True
                    self.left_count = 0

        # If blink start timer
        elif is_blink(left_closed, right_closed):
            if self.blink_start_time is None:
                self.blink_start_time = current_time

        else:
            # If blink timer > 1 second, switch mode
            if self.blink_start_time is not None:
                self.blink_duration = current_time - self.blink_start_time
                if self.blink_duration >= 1:
                    self.stop_gaze_tracking_flag = not self.stop_gaze_tracking_flag
                    self.stop_head_tracking_flag = not self.stop_head_tracking_flag
                self.reset_blink_timer()

            self.click_performed = False
            self.double_click_performed = False
            self.left_count = 0

    def reset_blink_timer(self):
        self.blink_start_time = None
        self.blink_duration = 0

    def set_cal(self, cal):
        self.left_cal, self.right_cal = cal

    def get_blink_duration(self):
        return self.blink_duration
