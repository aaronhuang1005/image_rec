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

cmd='CREATE TABLE IF NOT EXISTS login("memberid" TEXT,"ltime" TEXT);'
cur.execute(cmd)

'''
username="test"
cmd='INSERT INTO member values("'+ username +'","data/photo/'+username+'.jpg");'
cur.execute(cmd)

username="Aaron"
cmd='DELETE from member where memberid ="'+username+'";'
cur.execute(cmd)
'''

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
conn.close()