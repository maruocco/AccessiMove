"""Michael Ruocco, class for gaze and eye tracking using mediapipe"""
import cv2
import pyautogui
import mediapipe as mp


def map_value(value, from_range, to_range):
    """linear interpolation"""
    from_min, from_max = from_range
    to_min, to_max = to_range

    value = max(min(value, from_max), from_min)

    mapped_value = (value - from_min) / (from_max - from_min) * (to_max - to_min) + to_min

    return int(mapped_value)


"""create video and face points"""
cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

calibration_points = []

left_cal_dif = 0
right_cal_dif = 0
cal_w_i = 0
cal_h_i = 0
cal_w_b = 0
cal_h_b = 0
gaze_enabled = False
bridge_enabled = True
x_sens = 300
y_sens = 150

"""calibration captures single frame, can be adjusted later"""
for _ in range(1):
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks

    frame_h, frame_w, _ = frame.shape

    if landmark_points:
        landmarks = landmark_points[0].landmark
        calibration_points.append((landmarks[145].y, landmarks[159].y, landmarks[374].y, landmarks[386].y))
        left_cal_dif = (calibration_points[0][0] - calibration_points[0][1])
        right_cal_dif = (calibration_points[0][2] - calibration_points[0][3])

        cal_w_i = screen_w / frame_w * int(landmarks[474].x * frame_w)
        cal_h_i = screen_h / frame_h * int(landmarks[474].y * frame_h)

        cal_w_b = screen_w / frame_w * int(landmarks[168].x * frame_w)
        cal_h_b = screen_h / frame_h * int(landmarks[168].y * frame_h)

"""main loop"""
while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks

    frame_h, frame_w, _ = frame.shape

    if landmark_points:
        landmarks = landmark_points[0].landmark

        """using nose bridge for gaze"""
        if bridge_enabled:
            landmark = landmarks[168]
            x = landmark.x * frame_w
            y = landmark.y * frame_h
            screen_x = screen_w / frame_w * x
            screen_y = screen_h / frame_h * y
            x_low = cal_w_b - x_sens
            x_high = cal_w_b + x_sens
            y_low = cal_h_b - y_sens
            y_high = cal_h_b + y_sens
            x_move = map_value(screen_x, (x_low, x_high), (1, screen_w - 1))
            y_move = map_value(screen_y, (y_low, y_high), (1, screen_h - 1))
            pyautogui.moveTo(x_move, y_move)
            # pyautogui.moveTo(screen_x, screen_y)

        """using iris for gaze"""
        if gaze_enabled:
            for iris_id, landmark in enumerate(landmarks[474:478]):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                # cv2.circle(frame, (x, y), 3, (0, 255, 0))
                if iris_id == 1:
                    screen_x = screen_w / frame_w * x
                    screen_y = screen_h / frame_h * y
                    x_low = cal_w_i - x_sens
                    x_high = cal_w_i + x_sens
                    y_low = cal_h_i - y_sens
                    y_high = cal_h_i + y_sens
                    x_move = map_value(screen_x, (x_low, x_high), (1, screen_w - 1))
                    y_move = map_value(screen_y, (y_low, y_high), (1, screen_h - 1))
                    pyautogui.moveTo(x_move, y_move)

        """left wink"""
        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            # cv2.circle(frame, (x, y), 3, (0, 255, 255))

        """right wink"""
        right = [landmarks[374], landmarks[386]]
        for landmark in right:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            # cv2.circle(frame, (x, y), 3, (0, 255, 255))

        left_dif = left[0].y - left[1].y
        right_dif = right[0].y - right[1].y
        left_closed = left_dif < left_cal_dif / 2
        right_closed = right_dif < right_cal_dif / 2

        """"to prevent reading of blinks as winks"""
        if not (left_closed and right_closed):
            if left_dif < 0.004:
                pyautogui.leftClick()
                pyautogui.mouseDown()
            else:
                pyautogui.mouseUp()
            if right_dif < 0.004:
                pyautogui.rightClick()

    cv2.imshow('EyeControlled Mouse', frame)
    key = cv2.waitKey(1) & 0xFF
    """q to quit"""
    if key == ord('q'):
        break
    """press 'space' to toggle gaze tracking"""
    if key == ord(' '):
        gaze_enabled = not gaze_enabled
        x_sens = 90
        y_sens = 55
    """press m to toggle bridge tracking"""
    if key == ord('m'):
        bridge_enabled = not bridge_enabled
        x_sens = 300
        y_sens = 150

cam.release()
cv2.destroyAllWindows()
