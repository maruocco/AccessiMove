import asyncio
import pyautogui
import mediapipe as mp
import cv2

screen_w, screen_h = pyautogui.size()


def map_value(value, from_range, to_range):
    from_min, from_max = from_range
    to_min, to_max = to_range

    value = max(min(value, from_max), from_min)

    mapped_value = (value - from_min) / (from_max - from_min) * (to_max - to_min) + to_min

    return int(mapped_value)


async def gaze_tracking(frame, face_mesh, cal_w_i, cal_h_i, cal_w_b,
                        cal_h_b, x_sens, y_sens):
    frame_h, frame_w, _ = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks

    if landmark_points:
        landmarks = landmark_points[0].landmark

        # Gaze tracking using nose bridge
        landmark = landmarks[168]
        x = int(landmark.x * frame_w)
        y = int(landmark.y * frame_h)
        screen_x = screen_w / frame_w * x
        screen_y = screen_h / frame_h * y
        x_low = cal_w_b - x_sens
        x_high = cal_w_b + x_sens
        y_low = cal_h_b - y_sens
        y_high = cal_h_b + y_sens
        x_move = map_value(screen_x, (x_low, x_high), (1, screen_w - 1))
        y_move = map_value(screen_y, (y_low, y_high), (1, screen_h - 1))
        try:
            pyautogui.moveTo(x_move, y_move)
        except pyautogui.FailSafeException:
            print("Out of bounds")

        # Gaze tracking using iris
        # for iris_id, landmark in enumerate(landmarks[474:478]):
        #     x = int(landmark.x * frame_w)
        #     y = int(landmark.y * frame_h)
        #     if iris_id == 1:
        #         screen_x = screen_w / frame_w * x
        #         screen_y = screen_h / frame_h * y
        #         x_low = cal_w_i - x_sens
        #         x_high = cal_w_i + x_sens
        #         y_low = cal_h_i - y_sens
        #         y_high = cal_h_i + y_sens
        #         x_move = map_value(screen_x, (x_low, x_high), (1, screen_w - 1))
        #         y_move = map_value(screen_y, (y_low, y_high), (1, screen_h - 1))
        #         pyautogui.moveTo(x_move, y_move)


async def wink_detection(landmarks, left_cal_dif, right_cal_dif):
    left = [landmarks[145], landmarks[159]]
    right = [landmarks[374], landmarks[386]]

    left_dif = left[0].y - left[1].y
    right_dif = right[0].y - right[1].y
    left_closed = left_dif < left_cal_dif / 2
    right_closed = right_dif < right_cal_dif / 2

    if not (left_closed and right_closed):
        if left_dif < 0.004:
            pyautogui.leftClick()
        #     pyautogui.mouseDown()
        # else:
        #     pyautogui.mouseUp()
        if right_dif < 0.004:
            pyautogui.rightClick()


async def head_tilt_detection(landmarks):
    left_shoulder = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].x
    right_shoulder = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].x
    left_mouth = landmarks[mp.solutions.pose.PoseLandmark.MOUTH_LEFT.value].x
    right_mouth = landmarks[mp.solutions.pose.PoseLandmark.MOUTH_RIGHT.value].x

    nose = landmarks[mp.solutions.pose.PoseLandmark.NOSE.value].y
    shoulder = (landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].y +
                landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].y) / 2

    def calculate_distance(a, b):
        distance = a - b
        return distance

    left_distance = calculate_distance(left_shoulder, left_mouth)
    right_distance = calculate_distance(right_mouth, right_shoulder)
    nod_distance = calculate_distance(shoulder, nose)

    if left_distance < 0.15:
        pyautogui.press('right')
    elif right_distance < 0.15:
        pyautogui.press('left')
    elif nod_distance > 0.35:
        # pyautogui.press('up')  # Uncomment if you want to enable up tilt action
        pass
    elif nod_distance < 0.15:
        pyautogui.press('down')


async def main():
    cap = cv2.VideoCapture(0)
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    mp_pose = mp.solutions.pose

    calibration_points = []
    left_cal_dif = 0
    right_cal_dif = 0
    cal_w_i = 0
    cal_h_i = 0
    cal_w_b = 0
    cal_h_b = 0
    x_sens = 300
    y_sens = 150
    calibrated = False

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()

            if ret:
                frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
                frame.flags.writeable = False
                results = pose.process(frame)
                gesture_landmarks = results.pose_landmarks.landmark
                output = face_mesh.process(frame)
                landmark_points = output.multi_face_landmarks
                frame_h, frame_w, _ = frame.shape

                if landmark_points:
                    landmarks = landmark_points[0].landmark

                    if not calibrated:
                        calibration_points.append(
                            (landmarks[145].y, landmarks[159].y, landmarks[374].y, landmarks[386].y))

                        left_cal_dif = (calibration_points[0][0] - calibration_points[0][1])
                        right_cal_dif = (calibration_points[0][2] - calibration_points[0][3])

                        cal_w_i = screen_w / frame_w * int(landmarks[474].x * frame_w)
                        cal_h_i = screen_h / frame_h * int(landmarks[474].y * frame_h)

                        cal_w_b = screen_w / frame_w * int(landmarks[168].x * frame_w)
                        cal_h_b = screen_h / frame_h * int(landmarks[168].y * frame_h)
                        calibrated = True

                # Run different functions asynchronously
                tasks = [
                    gaze_tracking(frame, face_mesh, cal_w_i, cal_h_i,
                                  cal_w_b, cal_h_b, x_sens, y_sens),
                    wink_detection(landmarks, left_cal_dif, right_cal_dif),
                    head_tilt_detection(gesture_landmarks)
                ]

                await asyncio.gather(*tasks)

                # Display the combined video feed
                cv2.imshow('Combined Eye Tilt', frame)

                # Handle key events or any other non-asynchronous tasks
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    asyncio.run(main())
