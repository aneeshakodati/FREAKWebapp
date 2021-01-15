from pyrebase import pyrebase
from flask import (
    Flask,
    url_for,
    render_template,
    redirect,
    request
)
import cv2
from forms import SignUpForm
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
app=Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'

Config = {
  "apiKey": "AIzaSyC8vMBG6zv92CJVULsfBL4pV8Cd4ic8Scs",
  "authDomain": "freak-kiosk.firebaseapp.com",
  "databaseURL": "https://freak-kiosk-default-rtdb.firebaseio.com",
  "projectId": "freak-kiosk",
  "storageBucket": "freak-kiosk.appspot.com",
  "messagingSenderId": "1024973891229",
  "appId": "1:1024973891229:web:14d8cee0083d8ecb869674",
  "measurementId": "G-PWRT1VW54S"
  }
firebase=pyrebase.initialize_app(Config)
auth=firebase.auth()
db=firebase.database()
storage=firebase.storage()

cam=cv2.VideoCapture(0)


@app.route('/', methods=['GET', 'POST'])
def welcome():
    form=SignUpForm()
    if form.is_submitted():
        result=request.form
        try:
            auth.sign_in_with_email_and_password(str(form.email)[50:len(str(form.email))-2],(str(form.password)[56:len(str(form.password))-2]) )
        except:
            return render_template('wrongpasswordusername.html', result=result, form=form)
        return render_template('user.html', result=result)
    return render_template ('home.html', form=form)

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
            data={'Email': email, 'Password':password, 'Name':name, 'CardNo':cardno, 'CVV':cvv, 'Expiration Date': cardexp}
            db.child("users").child(email.replace(".","").replace("@", "").replace("_", "")).set(data)
            return render_template('facialrecognition.html', result=result)
        except:
            return render_template('user.html', result=result)
    return render_template('newaccount.html', form=form)

@app.route("/updateinfo", methods=['GET', 'POST'])
def updateinfo():
    form=SignUpForm()
    if form.is_submitted():
        result=request.form
        try:
            auth=sign_in_with_email_and_password (str(form.email)[50:len(str(form.email))-2], str(form.password)[56:len(str(form.password))-2])
            db.child("users").child(email_wnsc).update({'Password':str(form.password)[56:len(str(form.password))-2], 'Name':str(form.name)[48:len(str(form.name))-2], 'CardNo':str(form.creditCardNumber)[48:len(str(form.name))-2]})
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
