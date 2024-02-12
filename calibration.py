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

    def set_bounds(self, zone, landmark):
        self.zone = zone
        if zone == 4:
            self.c = landmark.x, landmark.y
            print(self.c)
        elif zone == 0:
            self.tl = landmark.x, landmark.y
            print(self.tl)
        elif zone == 1:
            self.tr = landmark.x, landmark.y
            print(self.tr)
        elif zone == 2:
            self.bl = landmark.x, landmark.y
            print(self.bl)
        elif zone == 3:
            self.br = landmark.x, landmark.y
            print(self.br)
        if self.br[0] != (0, 0):
            self.complete = True

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

    def set_frame_size(self, frame_size):
        self.frame_size = frame_size
