
# Python dlib 人臉辨識實作

本專題的參考書籍：*<Python機器學習超進化：AI影像辨識跨界應用實戰>*

## 第一步：臉部特徵點的定位

對於不太熟悉影像處理以及人工智慧架構和訓練的新手來說，能有現成的的工具可以使用能更快也更方便做出各種Demo。\
Python 中的 dlib 便是這種厲害的工具，不僅有現成的人臉辨識的演算法，更有官方提供的訓練模型檔，有利各種人工智慧的應用。\
\
首先必須先下載dlib，利用Python pip進行下載及安裝：

```
pip install dlib
```

當然這個僅有dlib的部分，實作中其他的模組都還要另外安裝。\
\
dlib 辨識的原理不得而知（至少我自己不清楚），但是在程式中可以稍微窺見以及大概瞭解中的演算法。\
先將模型檔 `shape_predictor_68_face_landmarks.dat` 讀入預測器並宣告偵測正面臉部的偵測器，語法如下：

```python=
predictor = dlib.shape_predictor(r"model/shape_predictor_68_face_landmarks.dat")
detector = dlib.get_frontal_face_detector()
```

模式應該是先將圖片放入偵測器得知正臉的位置，再由預測器預測臉部特徵點的位置。\
辨識的方法：

```python=
#img為輸入的影像
dets = detector(img,1)
result = predictor(img,det).parts()
```

`result` 便是辨識的結果，68點特徵點的座標，再依序將座標取出便可以使用結果。\
\
這部分我以webcam即時影像做測試，由攝像頭讀入影像，再承接上述的步驟，最後輸出影像，然後不段重複這個步驟直到使用者關閉，以下為程式碼：

```python=
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

#計算幀率的變數(執行一幀經過時間的倒數)
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

```

調皮的我在程式碼中加了許多開關，是因為我發現辨識的影響，原本攝像頭的幀率是60，但是辨識人特徵後，幀率下降至4~5

## 第二步：建立視窗

我自己的建立的方法適用Python內建的tkinter，但這部分的範圍較廣，我也是自己慢慢摸索，附上參考網址：[tkinter](https://steam.oxxostudio.tw/category/python/tkinter/start.html)\
\
這部分是想先測試攝像頭影像、臉部辨識以及視窗是否能正常運行，因此設計了以下的小視窗，可以顯示攝像頭畫面，辨識後的結果，並且可以開關上述的功能，如下圖：

![demo](https://hackmd.io/_uploads/BJsaDKFy6.png)

\
建立視窗其實照著教程做其實蠻簡單，建立視窗及設定特性：

```python=
root = tk.Tk()
root.geometry("736x561+479+178")
root.resizable(0, 0)
root.title("python dlib demo")
root.configure(background="#1f1f1f")
```

`root` 即是主視窗\
\
而按鈕的部分稍微複雜一些，需要設定觸發後的執行函式，而觸發後該函式更改檢查的布林變數，在執行中便只要判斷變數的值(其實只是把前一節的開關實體化按鈕)。以偵測開關為例，程式碼如下：

```python=
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
````

觸發函式 `dector_switch()`:

```python=
def dector_switch():
    if mode:
        global d
        d= not d
        if not d:
            detect.configure(text='''Detect''')
        else:
            detect.configure(text='''OFF''')
```

布林變數 `d` 便是執行時判斷的值。\
\
而要將攝像頭影像顯示於是窗上難度有些高，這部分式參考需多網路大神撰寫的結果。\
\
首先，必須先了解tkinter的視窗物件在設定完並執行後，是一個一直在執行的程序(loop)，如果要能看到即時影像，必須讓每次讀進來的影像都能寫入該視窗的Label物件(或是Canva物件)，但該視窗物件只能修改其特性(configure)，不過tkinter也提供了方法:

```
視窗物件.after(間隔時間,欲執行函式())
```

因此撰寫讀取攝像頭影像並寫入該視窗的Label物件的函式，再用此方法加入執行程序裡，便可以達到即時影像的顯示，而再加上上一節的顯示辨識結果的方法，即可完成本次的小測試目標，程式碼如下：

```python=
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
        
        #這裡原本想要用重新設定configure達到關掉鏡頭的效果，但似乎不行...
        videostream.configure(background="#d9d9d9")
        videostream.configure(disabledforeground="#a3a3a3")
        videostream.configure(foreground="#ffffff")
        videostream.configure(compound='center')
        videostream.configure(text='''Camera OFF''')
        
    root.update()

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
        
    #關鍵在這呢
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
```

## 第三步:建立資料庫

這邊用的資料庫跟書中相同，皆是sqlite，亦是用SQL存取。\
\
由於sqlite是一個檔案行資料庫，因此在本地端建立檔案便可以存取資料，程式碼如下:

```python=
conn = sqlite3.connect(r"data/member.sqlite")
cur=conn.cursor()
```

其中建立的 `cur` (資料庫的cursor)便可以執行SQL。\
\
資料庫的動作不外乎建立、插入、刪除資料，而為了方便資料庫的管理，我這裡撰寫了額外的程式，這邊可以作為存取的範例：

```python=
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 23:46:25 2023

@author: Aaron
"""

import sqlite3
import cv2

#-------------------------------------------------------------

conn = sqlite3.connect(r"data/member.sqlite")
cur=conn.cursor()

#-------------------------------------------------------------

cmd='CREATE TABLE IF NOT EXISTS member("memberid" TEXT PRIMARY KEY,"picture" TEXT);'
cur.execute(cmd)

#建立表格
cmd='CREATE TABLE IF NOT EXISTS login("memberid" TEXT,"ltime" TEXT);'
cur.execute(cmd)

#插入資料
username="test"
cmd='INSERT INTO member values("'+ username +'","data/photo/'+username+'.jpg");'
cur.execute(cmd)

#刪除資料
username="Aaron"
cmd='DELETE from member where memberid ="'+username+'";'
cur.execute(cmd)

#選擇資料
cmd='SELECT * FROM member;'
cur.execute(cmd)
rows=cur.fetchall()

index=0
for row in rows:
    index+=1
    print(index," ",row[1])
    img = cv2.imread(row[1])
    cv2.imshow("img",img)
    key = cv2.waitKey(0)

conn.commit()

#-------------------------------------------------------------
cv2.destroyAllWindows()

#關閉資料庫
conn.close()
```

以上便是資料庫的範例。

## 第四步：建立臉部登入系統

以上視窗、資料庫都測試成功，便可以開始撰寫登入系統。\
\
首先是首頁的部分，分為登入按鈕和註冊按鈕，各自連結到不同的頁面，
