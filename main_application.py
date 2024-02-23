# Michael Ruocco, Jack Duggan, main_application.py: Main class for AccessiMove program
import asyncio
import mediapipe as mp
import cv2
import time
import keyboard
from gaze_tracker import GazeTracker
from eye_controller import EyeController
from head_controller import HeadController
from calibration import Calibration
from boot_up import BootUp


class MainApplication:
    def __init__(self):
        self.gaze_tracker = GazeTracker()
        self.eye_controller = EyeController()
        self.head_controller = HeadController()
        self.calibration = Calibration()

    async def main(self):

        boot_up = BootUp("Images/logo.png")
        boot_up.display_image()

        cap = cv2.VideoCapture(0)
        face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
        mp_pose = mp.solutions.pose

        zone = 0
        cal_count = 0
        calibrated = False

        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                ret, frame = cap.read()

                if ret:
                    frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
                    frame.flags.writeable = False
                    results = pose.process(frame)
                    try:
                        gesture_landmarks = results.pose_landmarks.landmark
                        self.eye_controller.stop_head_tracking_flag = False
                    except:
                        self.eye_controller.stop_head_tracking_flag = True
                    output = face_mesh.process(frame)
                    landmark_points = output.multi_face_landmarks

                    if landmark_points:
                        landmarks = landmark_points[0].landmark
                        eye_landmarks = [landmarks[145].y, landmarks[159].y, landmarks[374].y, landmarks[386].y]
                        gaze_landmark = landmarks[168]

                        # calibrated = True

                        if not calibrated:

                            left_cal_dif = (eye_landmarks[0] - eye_landmarks[1])
                            right_cal_dif = (eye_landmarks[2] - eye_landmarks[3])
                            self.calibration.set_dif(left_cal_dif, right_cal_dif)

                            self.gaze_tracker.set_frame_size(frame.shape)
                            self.calibration.set_frame_size(frame.shape)

                            # print(f"look at {self.calibration.get_zone_name(zone)}.")
                            self.calibration.overlay_circle(zone)
                            time.sleep(1)

                            if cal_count % 2 == 1:
                                self.calibration.set_bounds(zone, gaze_landmark)
                                self.calibration.set_nod_thresh(zone, self.head_controller.get_nod_distance(
                                    gesture_landmarks, self.eye_controller.stop_head_tracking_flag))
                                zone += 1
                            cal_count += 1

                            if zone == 5:
                                self.gaze_tracker.set_calibration(self.calibration.get_bounds())
                                self.eye_controller.set_cal(self.calibration.get_dif())
                                self.head_controller.set_nod_cal(*self.calibration.get_nod_thresh())
                                self.calibration.set_complete(True)
                                calibrated = True

                        # Run different functions asynchronously
                        if calibrated:
                            tasks = [
                                self.gaze_tracker.gaze_tracking(gaze_landmark,
                                                                self.eye_controller.stop_gaze_tracking_flag),
                                self.eye_controller.wink_detection(eye_landmarks),
                                self.head_controller.detect_head_tilt(gesture_landmarks,
                                                                      self.eye_controller.stop_head_tracking_flag)
                            ]

                            await asyncio.gather(*tasks)

                    # Display the combined video feed
                    # cv2.imshow('Combined Eye Tilt', frame)

                    # Handle key events or any other non-asynchronous tasks
                    key = cv2.waitKey(1) & 0xFF
                    if keyboard.is_pressed('c'):
                        zone = 0
                        cal_count = 0
                        self.calibration.reset()
                        calibrated = False
                    elif keyboard.is_pressed('q'):
                        break
                    if key == ord('q'):
                        break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = MainApplication()
    asyncio.run(app.main())
