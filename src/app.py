from flask import Flask, render_template
from common.database import Database
from camera import take_picture
from facial_recognition import do_recognition
import datetime
import time

__author__ = 'lulis'

app = Flask(__name__)
app.secret_key = "123"
base_picture = "static/known_people/Lucas.png"

@app.before_first_request
def init_db():
    Database.initialize()

@app.route('/')
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
    user_name = do_recognition(base_picture, new_picture)
    entry_time = str(datetime.datetime.now())[:-7]
    data = {"user": user_name, "entry_time": entry_time, "photo": new_picture}
    Database.insert("entries", data)
    return render_template('welcome.html', user_name=user_name, 
                           entry_time=entry_time)
    
@app.route('/bye')
def bye():
    new_picture = take_picture()
    user_name = do_recognition(base_picture, new_picture)
    exit_time = str(datetime.datetime.now())[:-7]
    data = {"user": user_name, "exit_time": exit_time, "photo": new_picture}
    Database.insert("exits", data)
    return render_template('bye.html', user_name=user_name, 
                           exit_time=exit_time) 

app.run(debug=False, port=4990)