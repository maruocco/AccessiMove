# Michael Ruocco, calibration.py: This class stores the calibrated data from the user
import pygame
import win32api
import win32con
import win32gui
import numpy as np


class Calibration:

    def __init__(self):
        self.c = (0, 0)
        self.tl = (0, 0)
        self.tr = (0, 0)
        self.bl = (0, 0)
        self.br = (0, 0)
        self.xl = 1
        self.xr = 1
        self.yt = 1
        self.yb = 1
        self.cx = 1
        self.cy = 1
        self.complete = False
        self.zone = -1
        self.frame_size = (0, 0)
        self.left_cal_dif = 0
        self.right_cal_dif = 0
        self.left_dif_list = []
        self.right_dif_list = []

    def set_bounds(self, zone, landmark):
        self.zone = zone
        if zone == 4:
            self.c = landmark.x, landmark.y
        elif zone == 0:
            self.tl = landmark.x, landmark.y
        elif zone == 1:
            self.tr = landmark.x, landmark.y
        elif zone == 2:
            self.bl = landmark.x, landmark.y
        elif zone == 3:
            self.br = landmark.x, landmark.y

    def get_zone_name(self, zone):
        self.zone = zone
        match self.zone:
            case 0:
                return "top left"
            case 1:
                return "top right"
            case 2:
                return "bottom left"
            case 3:
                return "bottom right"
            case 4:
                return "center"

    def get_bounds(self):
        self.xl = ((self.tl[0] + self.bl[0]) / 2)
        self.xr = ((self.tr[0] + self.br[0]) / 2)
        self.yt = ((self.tl[1] + self.tr[1]) / 2)
        self.yb = ((self.br[1] + self.bl[1]) / 2)
        self.cx = (self.c[0])
        self.cy = (self.c[1])
        cal = [self.xl, self.xr, self.yt, self.yb, self.cx, self.cy]
        return cal

    def set_dif(self, left, right):
        self.left_dif_list.append(left)
        self.right_dif_list.append(right)
        self.left_cal_dif = np.mean(self.left_dif_list)
        self.right_cal_dif = np.mean(self.right_dif_list)

    def get_dif(self):
        return self.left_cal_dif, self.right_cal_dif

    def set_frame_size(self, frame_size):
        self.frame_size = frame_size

    def set_complete(self, complete):
        self.complete = complete
        pygame.quit()

    def overlay_circle(self, zone):
        self.zone = zone

        # Get the screen dimensions
        pygame.init()
        screen_info = pygame.display.Info()
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h

        radius = screen_width // 30
        position = (0, 0)

        match self.zone:
            case 0:
                position = (radius, radius)
            case 1:
                position = (screen_width - radius, radius)
            case 2:
                position = (radius, screen_height - radius)
            case 3:
                position = (screen_width - radius, screen_height - radius)
            case 4:
                position = ((screen_width // 2), (screen_height // 2))

        screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
        transparent_color = (255, 0, 0)  # Transparency color
        green = (0, 255, 0)

        # Create layered window
        hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                               win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        # Set window transparency color
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*transparent_color), 0, win32con.LWA_COLORKEY)

        screen.fill(transparent_color)  # Transparent background
        pygame.draw.circle(screen, green, position, radius)
        pygame.display.update()
