# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 16:53:02 2023

@author: Aaron
"""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import dlib
import sqlite3
import numpy as np

bg_width=1000
bg_height=750
head_width=129
head_height=135

mode=False
img_save=None

print("File_check-----------")
print("> Loading Model...")
predictor = dlib.shape_predictor(r"model/shape_predictor_68_face_landmarks.dat")
facerec = dlib.face_recognition_model_v1(r"model/dlib_face_recognition_resnet_model_v1.dat")
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

#-------------------------------------------------------------

front = tk.Tk()
front.geometry(str(bg_width)+"x"+str(bg_height)+"+480+180")
front.resizable(0, 0)
front.title("system")
front.configure(background="#1f1f1f")
front.iconbitmap(r"page_img/icon.ico")

backimg=ImageTk.PhotoImage(Image.open(r"page_img/background_1.jpg").resize((bg_width,bg_height)),master=front)
headimg=ImageTk.PhotoImage(Image.open(r"page_img/head.png").resize((head_width,head_height)),master=front)

background=tk.Canvas(front,width=bg_width,height=bg_height)
background.configure(background="#d9d9d9")
background.configure(bd=0)
background.configure(highlightthickness=0)
background.configure(relief="sunken")

background.create_image(0,0,anchor="nw",image=backimg)             #create background   

background.create_rectangle(350,140,646,602,width=0,fill="#252525")     #create bar

background.create_image(430,210,anchor="nw",image=headimg)         #create headimg

background.create_text(992, 742, text='Version：Dev-edition\nAuthor：Aaron Huang', anchor='se',fill='#dedede')
background.pack()

#-------------------------------------------------------------




#-------------------------------------------------------------


def log_func_name():
    
    global mode, backimg
    
    if not mode:
        
        mode=True
        
        def video_loop():
            
            global cap, img_save
            
            ret, img = cap.read()
            img = cv2.flip(img,1)
            img_save = img
            img1 = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            cv2.rectangle(img1, (170,74), (447, 413), (50,150,50), 5)
            current_img = Image.fromarray(img1)
            imgtk = ImageTk.PhotoImage(image=current_img)
            videostream.imgtk = imgtk
            videostream.configure(image = imgtk)
            log_name.after(1,video_loop)
        
        def img_feature(img_file):
            dets = detector(img_file,1)
            for det in dets:
                shape = predictor(img_file,det)
                feature = facerec.compute_face_descriptor(img_file, shape)
                return np.array(feature)
        
        def detect_image():
            global mode, img_save
            current_person = img_feature(img_save)
            
            same = False
            name=""
            for row in rows:
                #print(row)
                image = cv2.imread(row[1])
                data_person = img_feature(image)
                dist = np.linalg.norm(current_person - data_person)
                if dist < 0.4 :
                    same = True
                    name = row[0]
                    break
            if same:
                log_name.destroy()
                messagebox.showinfo('Success', name +' 登陸成功！')
                mode=False
            
            
        def con_closing():
            #print("close")
            global mode
            mode=False
            log_name.destroy()
        
       
    
        log_name = tk.Toplevel(front)
        log_name.geometry(str(bg_width)+"x"+str(bg_height)+"+500+200")
        log_name.resizable(0, 0)
        log_name.title("Log in")
        log_name.configure(background="#1f1f1f")
        log_name.iconbitmap(r"page_img/head.ico")
        
        
        background_sign = tk.Canvas(log_name,width=bg_width,height=bg_height)
        background_sign.configure(background="#d9d9d9")
        background_sign.configure(bd=0)
        background_sign.configure(highlightthickness=0)
        background_sign.configure(relief="sunken")
    
        background_sign.create_image(0,0,anchor="nw",image=backimg)             #create background   
    
        background_sign.create_text(992, 742, text='Version：Dev-edition\nAuthor：Aaron Huang', anchor='se',fill='#dedede')
        background_sign.pack()
        
        videostream = tk.Label(log_name)
        videostream.place(x=230, y=120, height=400, width=550)
        videostream.configure(anchor="center")
        videostream.configure(background="#1f1f1f")
        videostream.configure(foreground="#dedede")
        videostream.configure(compound='center')
        videostream.configure(font="-family {Arial} -size 9 -weight bold")
        videostream.configure(text=''' ''')
        
        save_button = tk.Button(log_name)
        save_button.place(x=450, y=550, height=34, width=88)
        save_button.configure(activebackground="#24305e")
        save_button.configure(activeforeground="black")
        save_button.configure(background="#353c73")
        save_button.configure(borderwidth="0")
        save_button.configure(command=detect_image)
        save_button.configure(compound='center')
        save_button.configure(disabledforeground="#6c6c6c")
        save_button.configure(font="-family {Arial} -size 9 -weight bold")
        save_button.configure(foreground="#e4e4e4")
        save_button.configure(highlightbackground="#a3a3a3")
        save_button.configure(highlightcolor="#050282")
        save_button.configure(pady="0")
        save_button.configure(text="log in")
        
        log_name.protocol("WM_DELETE_WINDOW", func=con_closing)
        
        conn = sqlite3.connect(r"data/member.sqlite")
        cur = conn.cursor()
        cmd = 'SELECT * FROM member;'
        cur.execute(cmd)
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        
        video_loop()
    
    else:
        messagebox.showwarning('Warning', '偵測其他視窗仍在運作，請確認是否正常關閉')
        
        
#-------------------------------------------------------------



#-------------------------------------------------------------

def sign_func(username):
    
    global mode, backimg
    
    if not mode:
        
        messagebox.showinfo('Sign Up Tips', '註冊須知:\n1.保持頭部在辨識區內\n2.盡量使影像不要晃動\n3.請確認面部朝向鏡頭，否則會註冊失效')
        
        #print("sign up")
        mode=True
        
        
        def video_loop():
            
            global cap, img_save
            
            ret, img = cap.read()
            img = cv2.flip(img,1)
            img_save = img
            img1 = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            cv2.rectangle(img1, (170,74), (447, 413), (50,150,50), 5)
            current_img = Image.fromarray(img1)
            imgtk = ImageTk.PhotoImage(image=current_img)
            videostream.imgtk = imgtk
            videostream.configure(image = imgtk)
            sign.after(1,video_loop)
            
            pass
        
        def save():
            global img_save
            global mode
            
            
            conn = sqlite3.connect(r"data/member.sqlite")
            cur=conn.cursor()
            
            cmd = 'INSERT INTO member values("'+ username +'","data/photo/'+username+'.jpg");'
            cur.execute(cmd)
            cv2.imwrite(r"data/photo/"+ username +".jpg",img_save)
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo('Success', '註冊成功！')
            mode = False
            sign.destroy()
        
        def close_func():
            #print("close")
            sign.destroy()
            
        def on_closing():
            global mode
            mode=False
            sign.destroy()
        
        sign = tk.Toplevel(front)
        sign.geometry(str(bg_width)+"x"+str(bg_height)+"+500+200")
        sign.resizable(0, 0)
        sign.title("Sign up")
        sign.configure(background="#1f1f1f")
        sign.iconbitmap(r"page_img/head.ico")
    
        background_sign = tk.Canvas(sign,width=bg_width,height=bg_height)
        background_sign.configure(background="#d9d9d9")
        background_sign.configure(bd=0)
        background_sign.configure(highlightthickness=0)
        background_sign.configure(relief="sunken")
    
        background_sign.create_image(0,0,anchor="nw",image=backimg)             #create background   
    
        background_sign.create_text(992, 742, text='Version：Dev-edition\nAuthor：Aaron Huang', anchor='se',fill='#dedede')
        background_sign.pack()
        
        videostream = tk.Label(sign)
        videostream.place(x=230, y=120, height=400, width=550)
        videostream.configure(anchor="center")
        videostream.configure(background="#1f1f1f")
        videostream.configure(foreground="#dedede")
        videostream.configure(compound='center')
        videostream.configure(font="-family {Arial} -size 9 -weight bold")
        videostream.configure(text=''' ''')
        
        save_button = tk.Button(sign)
        save_button.place(x=450, y=550, height=34, width=88)
        save_button.configure(activebackground="#24305e")
        save_button.configure(activeforeground="black")
        save_button.configure(background="#353c73")
        save_button.configure(borderwidth="0")
        save_button.configure(command=save)
        save_button.configure(compound='center')
        save_button.configure(disabledforeground="#6c6c6c")
        save_button.configure(font="-family {Arial} -size 9 -weight bold")
        save_button.configure(foreground="#e4e4e4")
        save_button.configure(highlightbackground="#a3a3a3")
        save_button.configure(highlightcolor="#050282")
        save_button.configure(pady="0")
        save_button.configure(text="Save")
        
        sign.protocol("WM_DELETE_WINDOW", func=on_closing)
        
        video_loop()
    else:
        messagebox.showwarning('Warning', '偵測其他視窗仍在運作，請確認是否正常關閉')
        
#-------------------------------------------------------------

def sign_name_func():
    
    global mode, backimg
    
    
    if not mode:
        
        mode=True
        
        def next_page_func():
            global mode
            check=False
            
            conn = sqlite3.connect(r"data/member.sqlite")
            cur=conn.cursor()
            
            cmd = 'SELECT * FROM member;'
            cur.execute(cmd)
            rows=cur.fetchall()
            
            text_name=input_name.get()
            
            #print(text_name)
            for row in rows:
                if row[0]==text_name:
                    messagebox.showwarning('Warning', '帳號名稱已被使用')
                    check=True
                    break
            if not check:
                mode=False
                sign_name.destroy()
                sign_func(text_name)
            conn.commit()
            conn.close()
            
        def con_closing():
            #print("close")
            global mode
            mode=False
            sign_name.destroy()
        
       
    
        sign_name = tk.Toplevel(front)
        sign_name.geometry(str(bg_width//2)+"x"+str(bg_height//2)+"+500+200")
        sign_name.resizable(0, 0)
        sign_name.title("Sign up")
        sign_name.configure(background="#1f1f1f")
        sign_name.iconbitmap(r"page_img/head.ico")
        
        
        background_sign = tk.Canvas(sign_name,width=bg_width,height=bg_height)
        background_sign.configure(background="#d9d9d9")
        background_sign.configure(bd=0)
        background_sign.configure(highlightthickness=0)
        background_sign.configure(relief="sunken")
    
        background_sign.create_image(0,0,anchor="nw",image=backimg)             #create background   
    
        background_sign.create_rectangle(120,125,400,223,width=0,fill="#252525")
        background_sign.create_text(992//2, 742//2, text='Version：Dev-edition\nAuthor：Aaron Huang', anchor='se',fill='#dedede')
        background_sign.create_text(130, 145, text='User name', anchor='nw',fill='#dedede',font="-family {Arial} -size 20 -weight bold")
        background_sign.pack()
    
        input_name = tk.Entry(sign_name,width=15)
        input_name.configure(background="#161616")
        input_name.configure(borderwidth="0")
        input_name.configure(disabledforeground="#a3a3a3")
        input_name.configure(font="-family {Arial} -size 15 ")
        input_name.configure(foreground="#d4d4d4")
        input_name.configure(insertbackground="#d4d4d4")
        input_name.configure(selectbackground="#354895")
        input_name.place(x=130, y=180)
        
        
        
        next_page = tk.Button(sign_name)
        next_page.place(x=295, y=180, height=25, width=88)
        next_page.configure(activebackground="#24305e")
        next_page.configure(activeforeground="black")
        next_page.configure(background="#353c73")
        next_page.configure(borderwidth="0")
        next_page.configure(command=next_page_func)
        next_page.configure(compound='center')
        next_page.configure(disabledforeground="#6c6c6c")
        next_page.configure(font="-family {Arial} -size 9 -weight bold")
        next_page.configure(foreground="#e4e4e4")
        next_page.configure(highlightbackground="#a3a3a3")
        next_page.configure(highlightcolor="#050282")
        next_page.configure(pady="0")
        next_page.configure(text="enter")
        
        sign_name.protocol("WM_DELETE_WINDOW", func=con_closing)
    
    else:
        messagebox.showwarning('Warning', '偵測其他視窗仍在運作，請確認是否正常關閉')
    
#-------------------------------------------------------------

log_Button = tk.Button(front)
log_Button.place(relx=0.44, rely=0.52, height=34, width=108)
log_Button.configure(activebackground="#4d1b17")
log_Button.configure(activeforeground="black")
log_Button.configure(background="#5b3939")
log_Button.configure(compound='left')
log_Button.configure(disabledforeground="#4d1b17")
log_Button.configure(font="-family {Franklin Gothic Demi Cond} -size 13")
log_Button.configure(foreground="#dedede")
log_Button.configure(borderwidth="0")
log_Button.configure(highlightbackground="#551515")
log_Button.configure(highlightcolor="#551515")
log_Button.configure(pady="0")
log_Button.configure(text='''Log in''')
log_Button.configure(command=log_func_name)

sign_Button = tk.Button(front)
sign_Button.place(relx=0.44, rely=0.613, height=34, width=108)
sign_Button.configure(activebackground="#24305e")
sign_Button.configure(activeforeground="black")
sign_Button.configure(background="#353c73")
sign_Button.configure(compound='left')
sign_Button.configure(disabledforeground="#0c0d3f")
sign_Button.configure(borderwidth="0")
sign_Button.configure(font="-family {Franklin Gothic Demi Cond} -size 13")
sign_Button.configure(foreground="#dedede")
sign_Button.configure(highlightbackground="#131564")
sign_Button.configure(highlightcolor="#131564")
sign_Button.configure(pady="0")
sign_Button.configure(text='''Sign up''')
sign_Button.configure(command=sign_name_func)

#-------------------------------------------------------------


#-------------------------------------------------------------

if __name__ == "__main__":
    front.mainloop()
    cap.release()
    

#-------------------------------------------------------------
