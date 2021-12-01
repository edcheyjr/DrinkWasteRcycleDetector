# import app gs
import flask
from app import app

import os
from resize import video_resize, image_resize
import urllib.request
from flask import  flash, request, redirect, abort, current_app
from werkzeug.utils import secure_filename
from os.path import join, splitext , exists
from predict import predict


vid_directory = "vids"
img_directory = "img"
resize_dir = "resized"

  
# Parent Directory path 
parent_dir = "/Users/edwin/Documents/WasteClassfication/yolov5/DrinkWasteWebDemo/frontend/static/uploads/"
  
# Path 
path = join(parent_dir, img_directory) 
  
# upload video or image
def upload_file_predict(
file, # file name
confidences
):
  path_list =[] # images predicted 
  confidences = int(confidences) /100
              
# resized dir
  upload_file_resized_vid_dir = join(app.config['UPLOAD_VID_FOLDER'],resize_dir )
  upload_file_resized_img_dir = join(app.config['UPLOAD_IMG_FOLDER'],resize_dir )
  for uploaded_files in request.files.getlist('file'):
    if uploaded_files.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    else:
    # sanitize te file name
        filename = secure_filename(uploaded_files.filename)
        file_ext = splitext(filename)[1]
        file_name = splitext(filename)[0]
        file_ext = file_ext.lower()

        if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        else:
    # vids
            # resized filename
            resized_filename = "{file_name}_resized{file_ext}".format(file_name=file_name, file_ext=file_ext)
            if file_ext in current_app.config['UPLOAD_VID_EXTENSIONS']:
                
                # join path and file name
                upload_file_path = join(app.config['UPLOAD_VID_FOLDER'], filename)
                if exists(app.config['UPLOAD_VID_FOLDER']) is False:
                  os.mkdir(app.config['UPLOAD_VID_FOLDER'])

                # test if the path exist
                if exists(upload_file_resized_vid_dir) is False:
                      # create the folder the create the path for the resized file to be saved
                    os.mkdir(upload_file_resized_vid_dir)
                    upload_file_resized_path = join(upload_file_resized_vid_dir,resized_filename)
                else:
                    upload_file_resized_path = join(upload_file_resized_vid_dir,resized_filename)

                # save original file
                uploaded_files.save(upload_file_path)

                # video resized
                video_resize(upload_file_path, upload_file_resized_path,
                current_app.config['SIZE'], 
                current_app.config['SIZE'],
                current_app.config['ASPECT_RATIO'])

                # predict
                predicted_classes, path_list = predict(
                  upload_file_path,
                  current_app.config['UPLOAD_IMG_EXTENSIONS'],
                  current_app.config['UPLOAD_VID_EXTENSIONS'],
                  current_app.config['WEIGHTS'],
                  confidences,
                  current_app.config['SAVE_DIR'],
                  current_app.config['SIZE']
                )
                #print('upload_video filename: ' + filename)
                flash('Video successfully uploaded and displayed below', 'message')
            

    # image
            elif file_ext in current_app.config['UPLOAD_IMG_EXTENSIONS']: 
              if exists(app.config['UPLOAD_IMG_FOLDER']) is False:
                  os.mkdir(app.config['UPLOAD_IMG_FOLDER'])
            
              # join path and file name
              upload_file_path = join(app.config['UPLOAD_IMG_FOLDER'], filename)
              # save original file
              uploaded_files.save(upload_file_path)
              # resized dir
          
                # test if the path exist
              if not exists(upload_file_resized_img_dir):
                  # create the folder the create the path for the resized file to be saved
                  os.mkdir(upload_file_resized_img_dir)
                  upload_file_resized_path = join(upload_file_resized_img_dir,resized_filename)
              else:
                  upload_file_resized_path = join(upload_file_resized_img_dir,resized_filename)

              if not exists(upload_file_resized_path):
              # use the save original file to create resized one
                image_resize(upload_file_path, upload_file_resized_path,current_app.config['SIZE'],current_app.config['SIZE'], current_app.config['ASPECT_RATIO'])

              
              predicted_classes, path = predict( 
                upload_file_path,
                current_app.config['UPLOAD_IMG_EXTENSIONS'],
                current_app.config['UPLOAD_VID_EXTENSIONS'],
                current_app.config['WEIGHTS'],
                confidences,
                current_app.config['SAVE_DIR'],
                current_app.config['SIZE'])
              path_list.append(path)

              print('upload_video filename: ' + filename)
              flash('Image successfully uploaded and tested')
            else:
              flash('does not accept that such of image or video data', 'error') 

  return predicted_classes,path_list