# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 19:51:25 2023

@author: Aaron
"""

import numpy as np
import cv2
import dlib
import time

predictor = dlib.shape_predictor(r"model/shape_predictor_68_face_landmarks.dat")
detector = dlib.get_frontal_face_detector()

start=0
end=0
status = False
d= False
print("set up complete")

cap = cv2.VideoCapture(1)
print("camera ready")


while True:
    start = time.time()
    ret, img = cap.read()
    img=cv2.flip(img,1)
    
    dets = detector(img,1)
    if d:
        for det in dets:
            landmark=[]
            for p in predictor(img,det).parts():
                landmark.append(np.matrix([p.x,p.y]))
            for idx, point in enumerate(landmark):
                pos = (point[0, 0], point[0, 1])
                cv2.circle(img, pos, 2, (255,255,255),-1)
                if status:
                    cv2.putText(img, str(idx+1), pos, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1, cv2.LINE_AA)
    end=time.time()
    cv2.rectangle(img, (0,0), (190, 55), (50,50,50), -1)
    cv2.putText(img, " Webcam frame: "+str(cap.get(cv2.CAP_PROP_FPS)), (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, " Real frame: "+str(1//(end-start)), (0, 43), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
    cv2.imshow("img",img)
    end = time.time()
    key = cv2.waitKey(1)
    if key == 27:
        break
    elif key == ord("n") or key == ord("N"):
        status = not(status)
    elif key == ord("d") or key == ord("D"):
        d = not(d)
cap.release()
cv2.destroyAllWindows()