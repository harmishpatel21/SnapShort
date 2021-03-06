import os
from app import app
import urllib.request
import flask
from flask import Flask, flash, request, redirect, url_for, render_template
from modules import ImageToText as IT
from modules import Model
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
# @app.route("/index")

def index():
    return flask.render_template('index.html')

@app.route('/', methods = ['POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Image successfully uploaded')
            text = IT.imageToText(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            summary = Model.main(text)
            return render_template('index.html', filename = filename, text = text, summary = summary)

        else:
            flash('Extensions not Allowed')
            return redirect(request.url)

# @app.route('/', methods= ['POST'])
# def generateSummary(text):

@app.route('/display/<filename>')
def display_image(filename):
    return render_template('index.html', url = './static/uploads/'+filename)

if __name__ == "main":
    app.run()
