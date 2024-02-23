# Michael Ruocco, gaze_tracker.py: This class handles gaze tracking and screen mapping
import win32api


# Linear interpolation function for mapping bridge coordinates to screen coordinates
def map_value(value, from_min, from_max, to_min, to_max, center=None):
    if center is not None:
        value -= center
        from_min -= center
        from_max -= center

    value = max(min(value, from_max), from_min)
    mapped_value = (value - from_min) / (from_max - from_min) * (to_max - to_min) + to_min

    return int(mapped_value)


class GazeTracker:
    def __init__(self):
        self.screen_w, self.screen_h = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
        self.x_move = self.screen_w / 2
        self.y_move = self.screen_h / 2
        self.to_x_range = (1, self.screen_w - 2)
        self.to_y_range = (1, self.screen_h - 2)
        self.from_x_range = (1, 2)
        self.from_y_range = (1, 2)
        self.center_x = 1
        self.center_y = 2
        self.frame_h, self.frame_w = (1, 1)
        self.screen_ratio_x = self.screen_w / self.frame_w
        self.screen_ratio_y = self.screen_h / self.frame_h
        self.smooth = 4
        self.avg_x = self.x_move
        self.avg_y = self.y_move
        self.alpha = 0.15

    def set_calibration(self, cal_h_w):
        self.from_x_range = ((cal_h_w[0] * self.screen_w), (cal_h_w[1] * self.screen_w))
        self.from_y_range = ((cal_h_w[2] * self.screen_h), (cal_h_w[3] * self.screen_h))
        self.center_x = (cal_h_w[4] * self.screen_h)
        self.center_y = (cal_h_w[5] * self.screen_h)

    def set_frame_size(self, frame_size):
        self.frame_h, self.frame_w, _ = frame_size
        self.screen_ratio_x = self.screen_w / self.frame_w
        self.screen_ratio_y = self.screen_h / self.frame_h

    async def gaze_tracking(self, landmark, gaze_track_flag):
        if landmark and not gaze_track_flag:

            # Gaze tracking using nose bridge
            x = int(landmark.x * self.frame_w)
            y = int(landmark.y * self.frame_h)
            screen_x = self.screen_ratio_x * x
            screen_y = self.screen_ratio_y * y
            mapped_x = map_value(screen_x, *self.from_x_range, *self.to_x_range, self.center_x)
            mapped_y = map_value(screen_y, *self.from_y_range, *self.to_y_range, self.center_y)

            # Update the cursor speed based on change in detected gaze distance
            self.avg_x = (1 - self.alpha) * self.avg_x + self.alpha * mapped_x
            self.avg_y = (1 - self.alpha) * self.avg_y + self.alpha * mapped_y

            # Setting new cursor position
            self.x_move = int(self.avg_x)
            self.y_move = int(self.avg_y)
            win32api.SetCursorPos((self.x_move, self.y_move))
