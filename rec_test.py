# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 14:27:40 2023

@author: Aaron
"""

import numpy as np
import cv2
import dlib
import time

predictor = dlib.shape_predictor(r"model/shape_predictor_68_face_landmarks.dat")
detector = dlib.get_frontal_face_detector()
print("set up complete")




start = time.time()
img = cv2.imread(r"data\photo\Aaron.jpg")
dets = detector(img,1)                      #detect the front face
for det in dets:        
    landmark=[]
    for p in predictor(img,det).parts():    #put the marked pic into 68 dot detector
        landmark.append(np.matrix([p.x,p.y]))
    for idx, point in enumerate(landmark):
        pos = (point[0, 0], point[0, 1])
        cv2.circle(img, pos, 2, (255,255,255),-1)
        #cv2.putText(img, str(idx+1), pos, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1, cv2.LINE_AA)
cv2.imshow("img",img)
key = cv2.waitKey(0)

cv2.destroyAllWindows()