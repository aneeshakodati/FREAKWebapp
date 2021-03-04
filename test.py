from pyrebase import pyrebase
from flask import (
    Flask,
    url_for,
    render_template,
    redirect,
    request
)

from forms import SignUpForm
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask import Flask, render_template, request, flash
import cv2
import cv2 as cv
import numpy as np
import imutils
import time
from imutils.video import VideoStream
from imutils.video import FPS
import os
from PIL import Image


def getImagesAndLabels(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    faceSamples=[]
    ids = []
    f=open("ids.txt", "a+")
    f1=f.readlines()
    id=0
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_numpy = np.array(PIL_img,'uint8')
        emailid = str(os.path.split(imagePath)[-1].split("~")[1])
        for x in f1:
            if(str(x.split("*")[-1])==emailid):
                id=int(x.split("*")[0])
        faces = detector.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
    return faceSamples,ids


f= open("ids.txt","r")
lines=f.readlines()
ids=0
for line in lines:
    print(line);
    if(int(line.split("*")[0])>int(ids)):
        ids=int(line.split("*")[0])
ids+=1
faceCascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")
video_feed = VideoStream(src=0).start()
time.sleep(2.0)
count = 0
email="kodatia@mcvts.net"
f=open("ids.txt", "a+")
f.write(str(ids)+"*"+email+"\n")
print("[INFO] Starting capture...")
while (True):
    if count >= 10:
        break
    frame = video_feed.read() #get webcam feed
    #frame = cv.flip(frame, -1)
    frame = imutils.resize(frame, width=500)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) #grayscale image
    found = faceCascade.detectMultiScale (gray, scaleFactor=1.1, minNeighbors=10, minSize = (30, 30)) #detect faces
    for (x,y,w,h) in found:
        cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        count += 1
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        cv.imwrite( "images/" +email+ '~' +
                    str(count) +
                    ".jpg", gray[y:y+h,x:x+w])
        #storage.child(email.replace(".","").replace("@", "").replace("_", "")).child("img" + '.' +str(count) +".jpg").put( "img" + '.' +str(count) +".jpg")
        print("stored image" + str(count))


video_feed.stream.release()
path = "images"
recognizer = cv.face.LBPHFaceRecognizer_create()
detector = cv.CascadeClassifier("haarcascade_frontalface_default.xml");
print("\n[INFO] Entering Training Stage...")
print ("[INFO] Training faces. It will take a few seconds. Wait...")
faces,ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids))
# Save the model into trainer/trainer.yml
recognizer.write('trainer.yml')
print("[INFO] {0} faces trained ...".format(len(np.unique(ids))))
