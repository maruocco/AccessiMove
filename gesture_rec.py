#Jack Duggan
#This program uses Mediapipe and cv2 libraries to capture head gestures from users and convert them into their respective arrow key inputs

import mediapipe as mp # Import mediapipe
import cv2 # Import opencv
import numpy as np
import autopy


mp_drawing = mp.solutions.drawing_utils 
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

tilt = False
#Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence =0.5) as pose:
    while cap.isOpened():
        ret,frame = cap.read()

        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False   

        #Make detection
        results = pose.process(image)

        #Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


        #print('on')
        #Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark

            #Get y-coords of shoulders and edges of mouth
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x
            left_mouth = landmarks[mp_pose.PoseLandmark.MOUTH_LEFT.value].x
            right_mouth = landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT.value].x

            nose = landmarks[mp_pose.PoseLandmark.NOSE.value].y
            shoulder = (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y + landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y)/2

            def calculate_distance(a,b):
                distance = a - b
                return distance
            
            #Calculate distance between shoulders and mouth edges
            left_distance = calculate_distance(left_shoulder,left_mouth)

            right_distance = calculate_distance(right_mouth,right_shoulder)

            nod_distance = calculate_distance(shoulder,nose)

            #print ('on')

            #Tilt Detection
            if left_distance < 0.15:
                tilt = True
                print("Left head tilt is", tilt)
                #autopy.key.tap(autopy.key.Code.LEFT_ARROW, delay = 0.5)
            elif right_distance < 0.15:
                tilt = True
                print("Right head tilt is", tilt)
                #autopy.key.tap(autopy.key.Code.RIGHT_ARROW, delay = 0.5)             
            elif nod_distance > 0.35:
                tilt = True
                print("Up head tilt is", tilt)
                #autopy.key.tap(autopy.key.Code.UP_ARROW, delay = 0.5)           
            elif nod_distance < 0.15:
                tilt = True
                print("Down head tilt is", tilt)
                #autopy.key.tap(autopy.key.Code.DOWN_ARROW, delay = 0.5)
            else: 
                print("No head tilt")
            
        except:
            pass

        #Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.imshow('MediaPipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()