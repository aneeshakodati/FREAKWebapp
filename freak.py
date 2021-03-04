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



app=Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'

Config = {
  "apiKey": "AIzaSyC6z8NHE2s9mg265PgOZNVsNuOJvQxkSzM",
  "authDomain": "free-ak-app.firebaseapp.com",
  "databaseURL": "https://free-ak-app-default-rtdb.firebaseio.com",
  "projectId": "free-ak-app",
  "storageBucket": "free-ak-app.appspot.com",
  "messagingSenderId": "1088930365757",
  "appId": "1:1088930365757:web:df1a7163b11981f7ec8554",
  "measurementId": "G-VKK8XKSWC7"
  }
firebase=pyrebase.initialize_app(Config)
auth=firebase.auth()
db=firebase.database()
storage=firebase.storage()

faceCascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")
recognizer = cv.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv.CascadeClassifier(cascadePath);
font = cv.FONT_HERSHEY_SIMPLEX

id = 0

@app.route('/', methods=['GET', 'POST'])
def welcome():
    file = open("ids.txt", "r")
    names = (file.read()).split()
    video_feed = VideoStream(src=0).start()
    print("\n[INFO] Entering Stream Stage...")
    print("[INFO] starting video stream...")
    time.sleep(2.0)
    fps = FPS().start()
    while ((cv.waitKey(1) & 0xFF) != ord("q")):
        frame = video_feed.read() #get webcam feed
        #frame = cv.flip(frame, -1)
        frame = imutils.resize(frame, width=500)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) #grayscale image
        found = faceCascade.detectMultiScale (gray, scaleFactor=1.1, minNeighbors=10, minSize = (30, 30)) #detect faces
        for(x,y,w,h) in found:
            cv.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            if (confidence < 100):
                id =str( names[id].split("*")[-1])
                print(id)
                information=db.child("users").child(id.replace("@", "").replace("_", "").replace(".", "")).get()
                fps.stop()
                video_feed.stream.release()
                return render_template('user.html', information=information.val())
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                fps.stop()
                video_feed.stream.release()
                form=SignUpForm()
                if form.is_submitted():
                    result=request.form
                    try:
                        auth.sign_in_with_email_and_password(str(form.email)[50:len(str(form.email))-2],(str(form.password)[56:len(str(form.password))-2]) )
                    except:
                        return render_template('wrongpasswordusername.html', result=result, form=form)
                    try:
                        email=str(form.email)[50:len(str(form.email))-2].replace(".", "").replace("@", "").replace("_", "").replace("-", "")
                        information=db.child("users").child(email).get()
                        return render_template('user.html', result=result, information=information.val())
                    except:
                        print("Error in getting information from database")
                return render_template('facenotrecognized.html', form=form)
    return render_template ('home.html', form=form)

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
        detector = cv.CascadeClassifier("haarcascade_frontalface_default.xml");
        faces = detector.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
    return faceSamples,ids
@app.route("/createaccount", methods=['GET', 'POST'])
def createAccount():
    form=SignUpForm()
    if form.is_submitted():
            result=request.form
            email=str(form.email)[50:len(str(form.email))-2]
            password=(str(form.password)[56:len(str(form.password))-2])
            name=str(form.name)[48:len(str(form.name))-2]
            cardno=str(form.creditCardNumber)[48:len(str(form.name))-2]
            cardexp= str(form.creditCardExpiration)[48:len(str(form.name))-2]
            cvv=str(form.cardCVV)[48:len(str(form.name))-2]
            try:
                auth.create_user_with_email_and_password(email, password )
                data={'email': email, 'password':password, 'name':name, 'creditCard':cardno, 'ccc':cvv, 'expiryDate': cardexp}
                db.child("users").child(email.replace(".","").replace("@", "").replace("_", "")).set(data)
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
                return render_template('facialrecognition.html', result=result)
            except:
                information=db.child("users").child(email.replace("@","").replace("_", "").replace(".", "").replace("-", "")).get()
                return render_template('user.html', result=result, information=information.val())
    return render_template('newaccount.html', form=form)

@app.route("/updateinfo", methods=['GET', 'POST'])
def updateinfo():
    form=SignUpForm()
    if form.is_submitted():
        result=request.form
        try:
            auth=sign_in_with_email_and_password (str(form.email)[50:len(str(form.email))-2], str(form.password)[56:len(str(form.password))-2])
            db.child("users").child(email_wnsc).update({'password':str(form.password)[56:len(str(form.password))-2], 'name':str(form.name)[48:len(str(form.name))-2], 'creditCard':str(form.creditCardNumber)[48:len(str(form.name))-2]})
            return render_template('facialrecognition.html', result=result)
        except:
            return render_template('wrongpasswordusername.html', result=result)
    return render_template('updateinfo.html', form=form)

def facialrecog(form, result):
    for i in range(1, 5):
        s, image=cam.read()
        if s:
            namedWindow("facial recognition image", CV_WINDOW_AUTOSIZE)
            imshow("facial recognition image", img)
            waitKey(0)
            destroyWindow("facial recognition image")
            filename="image"+str(i)+".jpg"
            imwrite(filename, img)
            storage.child(str(form.email)[50:len(str(form.email))-2]+"/facialrecog").put(filename)
        return render_template('facialrecognition.html', result=result)
if __name__=='__main__':
    app.run(debug=True)
