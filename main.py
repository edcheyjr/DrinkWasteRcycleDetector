# import app gs
import flask
from app import app

import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template, current_app, send_from_directory
from os.path import  splitext , basename
from upload import upload_file_predict

# route home
@app.route('/')
def index():
  return render_template('index.html')

# route mobile camera
@app.route('/phone-camera')
def camera():
  return render_template('camera.html')

# route aboutus
@app.route('/about-us')
def about():
  return render_template('about.html')

# route to form 
@app.route('/test-model')
def testModel():
  return render_template('upload.html')

# form request
@app.route('/test-model', methods=["POST"])
def submit_form():
  if request.method == 'POST':
    name = request.form['name']
    confidence = request.form['confidence']
    file = request.files['file'] 
    predicted_classes, path_list = upload_file_predict(file,confidence)
    
    # extract info from predicted classes
    print('predicted_classes',predicted_classes)
    # print('path list',path_list)
    return render_template('result.html', username = name, path_list=path_list, classes = predicted_classes)
            
    
# route to test imput 
@app.route('/test-result')
def result(): 
  return render_template('result.html')  



@app.route('/<filename>')
def display_images(filename): 
    file = basename(filename)
    file_ext = splitext(file)[1]
    # file_name = splitext(path)[0]
    if file_ext not in current_app.config['UPLOAD_IMG_EXTENSIONS']:
      flash('file not in the right format', 'error')        
      # do send the filepaths
      print('display image path: ' + file)
      print('path',filename)
    return redirect(url_for('static', filename=filename), code=301)
    


if __name__ == '__main__':
  app.run(debug=True, )
  # ssl_context = 'adhoc'  
  # host='192.168.93.72'  