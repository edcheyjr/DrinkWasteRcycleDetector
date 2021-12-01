# import flask
from flask import Flask
from os.path import join, dirname, realpath


UPLOAD_IMG_FOLDER = join(dirname(realpath(__file__)),'static/uploads/img/') # upload folder for images
UPLOAD_VID_FOLDER = join(dirname(realpath(__file__)), 'static/uploads/vids/') # upload folder for videos
WEIGHTS = './yolov5/weight/best.pt' # weight to use
UPLOAD_IMG_EXTENSION = ['.jpg', 'jpeg', '.png', '.gif'] # extensions accepted for images formats
UPLOAD_VID_EXTENSIONS =  ['.mp4', '.avi'] # extensions accepted for videos for video formats
SAVE_DETECTION_DIR = 'static/detect' # saving directory for detected images
SIZE = 640 # should be multiple of 32 to work well but i used 416 by 416 images for training testing and validation
MAX_CONTENT_LENGTH = 50 * 1024 * 1024 # a maximum of 52,428,800 bytes accepted

app = Flask(__name__)
app.secret_key = "MY_SECRET_KEY"
# aspect ratio will be maintained while true otherwise false while resizing
app.config['ASPECT_RATIO'] = True
 


# image and videos folder repectively
app.config['SAVE_DIR'] = SAVE_DETECTION_DIR
app.config['UPLOAD_IMG_FOLDER'] = UPLOAD_IMG_FOLDER
app.config['UPLOAD_VID_FOLDER'] = UPLOAD_VID_FOLDER
app.config['UPLOAD_IMG_EXTENSIONS'] = UPLOAD_IMG_EXTENSION
app.config['UPLOAD_VID_EXTENSIONS'] = UPLOAD_VID_EXTENSIONS
app.config['UPLOAD_EXTENSIONS'] = UPLOAD_IMG_EXTENSION + UPLOAD_VID_EXTENSIONS#['.jpg', 'jpeg', '.png', '.gif','.mp4', '.avi'] # TODO: merge upload video and upload images to be upload extensions
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['WEIGHTS'] = WEIGHTS
app.config['SIZE'] = SIZE

# required when serve video from static folder only
# return redirect(url_for('static', filename='uploads/' + filename), code=301)
