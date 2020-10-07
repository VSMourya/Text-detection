from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np
import time 
# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
# Define a flask app

app = Flask(__name__,  static_url_path = "/static", static_folder = "static")


IMAGE_FOLDER = 'static'
SAVE_FOLDER = 'uploads'
# app.config['IMAGE_FOLDER'] = IMAGE_FOLDER
# app.config['SAVE_FOLDER'] = SAVE_FOLDER



def text_detection(imgName):
    os.system(f'python3 test.py --trained_model=craft_ic15_20k.pth  --test_img=uploads/{imgName} --cuda=False')


@app.route('/', methods=['GET','POST'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/home', methods=['GET','POST'])
def home():
    return render_template('index.html')


@app.route('/predict', methods=['GET','POST'])
def predict():


    if request.method == "GET":
        print("GET ME AAGAYE BHAI ")



    if request.method == 'POST':
        # Get the file from post request
        f = request.files['image']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_name = secure_filename(f.filename)
        file_path = os.path.join("uploads", file_name)
        f.save(file_path)

        # Make prediction
        text_detection(file_name)


        # output_file_path = os.path.join(app.config["IMAGE_FOLDER"],file_name)
        output_file_path = "res_" + file_name.split(".")[0] + ".png"
        print("==========================================")
        
        return render_template("show.html", output_file_path = output_file_path)

    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)

