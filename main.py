import subprocess

import threading
import gesture_rec # Assuming you saved your provided class in a file named mediapipe_pose_class.py
# Import the second class here

class PoseDetectionWrapper:
    def __init__(self):
        self.pose_detection = gesture_rec.PoseDetection()

    def run(self):
        self.pose_detection.start_pose_detection()

# Add the second class wrapper here

def main():
    # Create instances of the wrapper classes
    pose_detection_wrapper = PoseDetectionWrapper()
    # Create an instance of the second class wrapper

    # Create threads for each class
    thread1 = threading.Thread(target=pose_detection_wrapper.run)
    # Create a thread for the second class wrapper

    # Start the threads
    thread1.start()
    # Start the second thread

    # Wait for the threads to finish
    thread1.join()
    # Join the second thread

def run_splash_screen():
    subprocess.call(["python", "boot_up.py"])


def run_eye_track():
    subprocess.call(["python", "eye_track.py"])


if __name__ == "__main__":
    main()
    #run_splash_screen()
    #run_eye_track()

