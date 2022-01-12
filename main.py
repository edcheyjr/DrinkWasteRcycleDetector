# import app gs
# from flask.helpers import make_response
from app import app
from werkzeug.datastructures import FileStorage
# import urllib.request
from flask import flash, request, redirect, url_for, render_template, current_app, jsonify, make_response
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
from os.path import  splitext , basename
from base64Topng import base64ToPngConverter
from upload import upload_file_predict
from os import _exit, path
# define RESTFul api
CORS(app)
api = Api(app)

# blobs array
BLOBS = []

# route home
@app.route('/')
def index():
  return render_template('index.html')

# get blob
class Blob(Resource):
    # def get(self, blob_id):
    #   abort_if_todo_doesnt_exist(blob_id)
    #   return {blob_id: BLOBS[blob_id]}
    def post(self):

      blob = request.get_json()
      # print(blob)

      BLOBS.append(blob)
      # convert base64 to png
      if blob is not None:
        req = make_response(jsonify({"message":"Blob as been recieved"}),200)
        for b in BLOBS:
          img_data = b['blob']
          img_id = b['blob_id']
          image_file = base64ToPngConverter(img_data, img_id)
          # print(image_file)
          # print(type(image_file))
  
          confidence = 40
          predicted_classes_dict,path_list,is_video = upload_file_predict(confidence,image_file)
          # extract info from predicted classes
          print('predicted_classes',predicted_classes_dict)            
          print('pathlist:',path)
        return render_template('result.html', username = "Edwin", classes = predicted_classes_dict, path_list= path_list, is_video=is_video)
      else:
        err = make_response(jsonify({"error":"No json received"}), 400)  
        return err

api.add_resource(Blob, '/camera/blob')  

# camera route
@app.route('/phone-camera')
def camera():    # file = request.files['file'] 
    # predicted_classes, path_list = upload_file_predict(file,confidence)
    
    # extract info from predicted classes
    # print('predicted_classes',predicted_classes)
    # print('path list',path_list)
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
    # print(file)
    # print(type(file))
    predicted_classes_dict,path_list, is_video= upload_file_predict(confidence)
    
    # extract info from predicted classes
    print('predicted_classes_dict',predicted_classes_dict)
    # print('path list',path_list)
    return render_template('result.html', username = name, classes = predicted_classes_dict, path_list = path_list, is_video=is_video)         
    
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
  app.run(debug=True)
  #  host='192.168.226.72'
  #  ssl_context = 'adhoc'