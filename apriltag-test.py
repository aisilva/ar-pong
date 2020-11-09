import sys
import cv2
import apriltag
import numpy as np



CAMERA_INDEX = 0
cap = cv2.VideoCapture(CAMERA_INDEX)

at_detector = apriltag.Detector()

while True:
    _, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    tags = at_detector.detect(gray)

    if len(tags) != 0:
        for tag in tags[0:2]:
            print("Tag ID: {}".format(tag.tag_id))
            print(np.linalg.norm(tag.corners[0] - tag.corners[1]))
            
            corners = np.array(tag.corners, np.int32)
            cv2.polylines(frame, [corners], True, (0, 255, 0), thickness=5)
            
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
