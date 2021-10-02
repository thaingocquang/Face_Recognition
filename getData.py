import cv2
import numpy as np
import sqlite3
import os

def insertOrUpdate(id, name):
    conn = sqlite3.connect('D:\\NDKM\\data.db')
    query = "SELECT * FROM people WHERE ID=" + str(id)
    cursor = conn.execute(query)
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
    if(isRecordExist==0):
        query = "INSERT INTO people(ID, Name) VALUES(" + str(id) + ", '" + str(name) + "')"
    else:
        query = "UPDATE people SET Name='" + str(name) + "' WHERE ID =" + str(id)
    conn.execute(query)
    conn.commit()
    conn.close()

# load tv
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
#insert to db
id = input("Enter your ID: ")
name = input("Enter your Name: ")
insertOrUpdate(id,name)
sampleNum = 0
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
        if not os.path.exists('D:/NDKM/dataSet'):
            os.makedirs('D:/NDKM/dataSet')
        sampleNum += 1
        cv2.imwrite('D:/NDKM/dataSet/User.' + str(id) + '.' + str(sampleNum) + '.jpg', gray[y:y+h, x:x+w])
    cv2.imshow('frame', frame)
    cv2.waitKey(1)
    if sampleNum>100:
        break
cap.release()
cv2.destroyAllWindows()
