import base64
from app import app
from os.path import exists
import os


def base64ToPngConverter(img_data, img_id):
    arr = img_data.split(';')
    data = arr[0]
    base64_bytes = arr[1]
    data_type = data.split(':')[1]
    print(data_type)
    if data_type == 'image/png':
        base64_bytes_data = base64_bytes.split(',')[1]
        if exists(app.config['UPLOAD_IMG_FOLDER']) is False:
            os.mkdir(app.config['UPLOAD_IMG_FOLDER'])
        image_path = "./static/uploads/img/capture_{}.png".format(img_id)
        with open(image_path, "wb") as fh:
            fh.write(base64.b64decode(base64_bytes_data))
    else:
        if exists(app.config['UPLOAD_VID_FOLDER']) is False:
            os.mkdir(app.config['UPLOAD_VID_FOLDER'])
        print(base64_bytes)
        video_path = "{}recording_{}.mp4".format(
            app.config['UPLOAD_VID_FOLDER'], img_id)
        with open(video_path, "rb") as videoFile:
            text = base64.b64encode(videoFile.read())
            print(text)
            file = open("textTest.txt", "wb")
            file.write(text)
            file.close()

            fh = open("video.mp4", "wb")
            fh.write(base64.b64decode(text))
            fh.close()
    return image_path
