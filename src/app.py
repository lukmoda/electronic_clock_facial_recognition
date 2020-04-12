from flask import Flask, render_template, redirect, url_for, request
from common.database import Database
from camera import take_picture
from facial_recognition import do_recognition
import os
import datetime
import time

__author__ = 'lucas moda'
app = Flask(__name__)

#List of Employees (base pictures names)
base_pictures = []
for root, _, files in os.walk("static/known_people/"):
    for filename in files:
        base_pictures.append(root + filename)

@app.before_first_request
def init_db():
    Database.initialize()
    
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if Database.find_one('users', {"username": "{user}".format(user=request.form['username']), "password": "{pwd}".format(pwd=request.form['password'])}) == None:
            error = 'Invalid Credentials. Please try again.'
        else:
            global user_logged 
            user_logged = request.form['username']
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/insert_photo_welcome')
def insert_photo_w():
    return render_template('insert_photo_w.html')

@app.route('/insert_photo_exit')
def insert_photo_e():
    return render_template('insert_photo_e.html')

@app.route('/welcome')
def welcome():
    new_picture = take_picture()
    base_picture = [picture for picture in base_pictures if user_logged.casefold() in picture.casefold()][0]
    user_name, match = do_recognition(base_picture, new_picture)
    if match == True:        
        entry_time = str(datetime.datetime.now())[:-7]
        data = {"user": user_name, "entry_time": entry_time, "photo": new_picture}
        Database.insert("entries", data)
        return render_template('welcome.html', user_name=user_name, 
                            entry_time=entry_time) 
    else:
        return render_template('fail.html')
    
@app.route('/bye')
def bye():
    new_picture = take_picture()
    base_picture = [picture for picture in base_pictures if user_logged.casefold() in picture.casefold()][0]
    user_name, match = do_recognition(base_picture, new_picture)
    if match == True:        
        exit_time = str(datetime.datetime.now())[:-7]
        data = {"user": user_name, "exit_time": exit_time, "photo": new_picture}
        Database.insert("exits", data)
        return render_template('bye.html', user_name=user_name, 
                            exit_time=exit_time) 
    else:
        return render_template('fail.html')

app.run(debug=False, port=4990)