# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 01:57:10 2023

@author: Aaron
"""

import tkinter as tk
import cv2
from PIL import Image, ImageTk
import dlib
import numpy as np

def out():
    global mode
    global out_text
    if not mode:
        mode=not mode
        out_text='''OFF'''
        cameraswitch.configure(text=out_text)
        videostream.configure(text=" ")
    else:
        mode=not mode
        out_text='''ON'''
        cameraswitch.configure(text=out_text)
        cameraswitch.configure(font="-family {Arial} -size 9 -weight bold")
        videostream.configure(background="#d9d9d9")
        videostream.configure(disabledforeground="#a3a3a3")
        videostream.configure(foreground="#ffffff")
        videostream.configure(compound='center')
        videostream.configure(text='''Camera OFF''')
    root.update()
    root.update_idletasks()

def video_loop():
    global cap
    global predictor, detector
    global d, status
    global mode
    if mode:
        ret, img = cap.read()
        img=cv2.flip(img,1)
        if d:
            dets = detector(img,1)
            for det in dets:
                landmark=[]
                for p in predictor(img,det).parts():
                    landmark.append(np.matrix([p.x,p.y]))
                for idx, point in enumerate(landmark):
                    pos = (point[0, 0], point[0, 1])
                    cv2.circle(img, pos, 2, (255,255,255),-1)
                    if status:
                        cv2.putText(img, str(idx+1), pos, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1, cv2.LINE_AA)
        img1=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        current_img=Image.fromarray(img1)
        imgtk=ImageTk.PhotoImage(image=current_img)
        
        #print(mode)
        
        videostream.imgtk=imgtk
        videostream.configure(image=imgtk)
    root.after(1,video_loop)
    
def number_switch():
    if mode and d:
        global status
        status= not status
        if not status:
            numberswitch.configure(text='''123''')
        else:
            numberswitch.configure(text='''OFF''')
        
    
def dector_switch():
    if mode:
        global d
        d= not d
        if not d:
            detect.configure(text='''Detect''')
        else:
            detect.configure(text='''OFF''')

print("File_check-----------")
print("> Loading Model...")
predictor = dlib.shape_predictor(r"model/shape_predictor_68_face_landmarks.dat")
detector = dlib.get_frontal_face_detector()
print("> Complete.")
print("---------------------\n")

camera=None

while True:
    try:
        print("Camera_check---------")
        camera=int(input("> Enter the camera number:"))
        print("> Setting Camera...")
        cap = cv2.VideoCapture(camera)
        print("> Complete.")
        print("---------------------\n")
        break
    except:
        camera=None
        print("> Setting Camera error")
        print("---------------------\n")


mode=False
out_text='''ON'''
status = False
d= False

root = tk.Tk()
root.geometry("736x561+479+178")
root.resizable(0, 0)
root.title("python dlib demo")
root.configure(background="#1f1f1f")

videostream = tk.Label(root)
videostream.place(relx=0.167, rely=0.089, height=350, width=511)
videostream.configure(background="#d9d9d9")
videostream.configure(disabledforeground="#a3a3a3")
videostream.configure(foreground="#000000")
videostream.configure(compound='center')
videostream.configure(font="-family {Arial} -size 9 -weight bold")
videostream.configure(text='''Camera OFF''')

cameraswitch = tk.Button(root)
cameraswitch.place(relx=0.45, rely=0.81, height=34, width=88)
cameraswitch.configure(activebackground="beige")
cameraswitch.configure(activeforeground="black")
cameraswitch.configure(background="#03015c")
cameraswitch.configure(borderwidth="5")
cameraswitch.configure(command=out)
cameraswitch.configure(compound='center')
cameraswitch.configure(disabledforeground="#6c6c6c")
cameraswitch.configure(font="-family {Arial} -size 9 -weight bold")
cameraswitch.configure(foreground="#e4e4e4")
cameraswitch.configure(highlightbackground="#a3a3a3")
cameraswitch.configure(highlightcolor="#050282")
cameraswitch.configure(pady="0")
cameraswitch.configure(text=out_text)

numberswitch = tk.Button(root)
numberswitch.place(relx=0.177, rely=0.82, height=24, width=48)
numberswitch.configure(command=number_switch)
numberswitch.configure(activebackground="beige")
numberswitch.configure(activeforeground="black")
numberswitch.configure(background="#b65547")
numberswitch.configure(compound='left')
numberswitch.configure(disabledforeground="#a3a3a3")
numberswitch.configure(foreground="#e4e4e4")
numberswitch.configure(highlightbackground="#d9d9d9")
numberswitch.configure(highlightcolor="black")
numberswitch.configure(pady="0")
numberswitch.configure(text='''123''')

detect = tk.Button(root)
detect.place(relx=0.272, rely=0.82, height=24, width=60)
detect.configure(activebackground="#0d8a55")
detect.configure(command=dector_switch)
detect.configure(activeforeground="black")
detect.configure(background="#0d8a55")
detect.configure(compound='left')
detect.configure(disabledforeground="#a3a3a3")
detect.configure(foreground="#e4e4e4")
detect.configure(highlightbackground="#d9d9d9")
detect.configure(highlightcolor="black")
detect.configure(pady="0")
detect.configure(text='''Detect''')


video_loop()
root.mainloop()

cap.release()
cv2.destroyAllWindows()