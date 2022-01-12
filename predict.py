
import torch
from os.path import splitext,basename,exists, join
from PIL import Image
import cv2
from app import app
import os
import numpy as np
 
# check whether the data is from web cam or photos uploaded
 # python detect.py --weight   --source 0  # webcam
 #                            file.jpg  # image 
 #                            file.mp4  # video
 #                            path/  # directory
 #                            path/*.jpg  # glob
 #                            rtsp://170.93.143.139/rtplive/470011e600ef003a004ee33696235daa  # rtsp stream
 #                            rtmp://192.168.1.105/live/test  # rtmp stream
 #                            http://112.50.243.8/PLTV/88888888/224/3221225900/1.m3u8  # http stream
# !python detect.py --source '/kaggle/input/v2-balloon-detection-dataset/images' --weights 'runs/train/exp/weights/best.pt' --img 640 --save-txt --save-conf --exist-ok


# predict function
'''
This function does the preodiction for both videos and images
'''

def predict(
  data_path, #data path
  img_ext = app.config['UPLOAD_IMG_EXTENSIONS'], # image extensions
  vids_ext = app.config['UPLOAD_VID_EXTENSIONS'], # vid extensions
  weight_path = None, # weight path eg. './yolov5/weight/best.pt'
  model_conf = 0.3,  # model confidence
  save_dir= 'static/detect', # detect path 
  size = 640, # default 416
  objects_detected = [], # objects detected array need to be passed in order to get the dffetent class of the images
  enumerate = 0 , #number of loop depending on the number of images being selected used by the objects_detected to insert classes depending on the keys 
  webcam = False, # webcam
):
  # model setup
  # load model in its own environment loading locally for now


  model = torch.hub.load('./yolov5', 'custom', source='local', path=weight_path ) # for PIL/cv2/np inputs and  
  # confidences
  model.conf = model_conf

  # use cpu instead of cuda 
  model.cpu()
  # data to be infered is stores hre
  data =[]
  # batch of images stored here
  imgs =[]
  # videos url stores here
  vids =[]

  
  # image dictionary
 
#  array to store other dictionary for all images and videos uploaded
  # objects_detected = []
  # append data path to the data
  data.append(data_path)

  vids_save_dir= save_dir +'/vids/'
  imgs_save_dir=  save_dir +'/img/'
  

  i=0

  for f in data:
    if exists(f):
      file_basename = basename(f)
      file_ext = splitext(file_basename)[1]
      file_name = splitext(file_basename)[0]
      file_ext = file_ext.lower()
      print(file_ext)

      # dict to store objects detected
      img_objects_detect = {}

      # ['.jpg', '.png', './.jpg']
      if file_ext in img_ext and webcam is False:
        # img1 = Image.open(f)  # PIL image
        img = cv2.imread(f)[..., ::-1]  # OpenCV image (BGR to RGB)
        imgs.append(img)
        # Inference
        results = model(imgs, size=size)  # includes NMS
        # store class predicted
        new_df = results.pandas()
        print(new_df)
        new_result = new_df.xywh[0]['name']
        classes = new_result.tolist()
        print(classes)
        # print and save results
        results.print()
        new_exp_dir = 'new_img_exp'+str(i)
        new_imgs_save_dir = join(imgs_save_dir ,new_exp_dir)
        print(new_imgs_save_dir) 
        if exists(imgs_save_dir):
          for n in range(0,len(os.listdir(imgs_save_dir))):
            # print(len(os.listdir(imgs_save_dir)))
            # print('loop times', n+1)
            new_exp_dir = 'new_img_exp'+str(n+1)
            new_imgs_save_dir = join(imgs_save_dir , new_exp_dir) 
            print(new_imgs_save_dir)
            if not exists(new_imgs_save_dir):
              results.save(new_imgs_save_dir)
              
        else:
          results.save(new_imgs_save_dir)
        # append the path of predicted images for display
        save_dir_arr = []
        save_dir_arr = new_imgs_save_dir.split('/')
        detect_dir = join(save_dir_arr[1], save_dir_arr[2], save_dir_arr[3])
        value_list = []
        class_list =[]
        list_image_path =[]
      # store all the info into a dict
        path =join(detect_dir,'image0.jpg').replace('\\','/') #replace all backslashes woth forward slash
        if classes:
          for iterate in classes:
            if iterate not in class_list:
              class_list.append(iterate)
              value_list.append(1)
            else:
              value_list[len(class_list)-1] += 1

          # list_image_path.append(path)    #image list
          value_list.insert(-1,value_list[len(class_list)-1])
          value_list.pop(len(class_list)-1)
        else:
          class_list.append('no class identified')
          value_list.append(0)
        img_objects_detect['class'] = class_list
        img_objects_detect['value'] = value_list
        img_objects_detect['imagePath'] = path

        # return img_objects_detect, image_path # classes predicted list, image_path of predicted image str
        # results.show() ['.mp4', '.avi']
      elif file_ext in vids_ext and webcam is False:

        #  read the video file
        # append all the videos to be inferenced
        vids.append(f)
        # Inference
        for vid in vids:
          img_objects_detect, list_image_path =detect_video(model,vid,file_name,vids_save_dir)
        # check_dict.save('static/detect/vids')  
      elif webcam is True:
      # TODO: create script to open webcam
        command ='!python detect.py --weights weight_path  --conf model_conf --source 0 --project ./static/detect/ --name vids' 
      else:
        print('do nothing')
        path =''
      # append the dictionary to this list
      objects_detected.insert(enumerate,img_objects_detect)
      print('objects_detected', objects_detected)
      
        # print and save results  
    else:
      error_file_path = "file doesn/'t exist"
      print(error_file_path)
  # return path and all object detected in the videos or images 
  return objects_detected, list_image_path

# video predict
# function detect video frames
def detect_video(
model, # model
video_path,# video path
file_name, #file name
save_dir = None # save path
):  
    list_of_frames_path = [] # path list
    list_frames_imgs = [] # frames to be processed to video
    list_of_original_frames = [] # list of original frames
    list_of_detected_classes_in_all_frames = [] #classes dtected list
    detected_classes = []
    check_dict = {}
    # i for naming each detected frame
    i=0

    print(video_path)
    cap = cv2.VideoCapture(video_path)
    if (cap.isOpened() is False):
        print("Error opening the video file")
        # Read fps and frame count
    else:
        # video info
        # use 5 or CAP_PROP_FPS
        fps = cap.get(cv2.CAP_PROP_FPS)        
        print('Frames per second : ', fps,'FPS')
        # You can replace 7 with CAP_PROP_FRAME_COUNT as well, they are enumerations
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        print('Frame count : ', frame_count)
        while (cap.isOpened()):
          ret, frame = cap.read()
          if ret == False:
              break      
            # cv2.imshow('Frame',frame)
          frame = frame[..., ::-1] # refine the frames from OpenCV image (BGR to RGB)    
          list_of_original_frames.append(frame)
            # cv2.imshow('Frame',frame)
        cap.release()
        cv2.destroyAllWindows()

    for file in list_of_original_frames:
        print('frame {} out of {}'.format(i,frame_count))
        # predict
        results = model(file)
        results.print()
        print(type(results.pred))
        tensor = torch.stack(results.pred)
        # print(type(tensor))
        print(tensor)
        empty_tensor = torch.empty(1,0,6)

        print(empty_tensor)
    
        # equate if they are the same it will be true otherwise false
        is_empty = torch.equal(tensor,empty_tensor)
        # if the tensor is not empty meaning their was prediction save otherwise dont meaning false
        if not is_empty:
            name = file_name+'_frame_'+str(i)
            path = save_dir+name
            save_dir_arr = []
            save_dir_arr = save_dir.split('/')
            print(save_dir_arr)
            detect_dir = join(save_dir_arr[1], save_dir_arr[2])
            new_path = join(detect_dir,name)
            results.save(path)
            print(new_path)

            # TODO: convert the frames to video
            # img = cv2.imread(path)
            # print(type(img))
            # height, width, layers = img.shape 
            # size = (width,height)
            # out = cv2.VideoWriter('./static/vids/preject.mp4',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
            # img.append(img)
            
            i+=1

            # save all predicted frames path to a list
            image_path = join(new_path,'image0.jpg').replace('\\', '/') # remove backslashes and replaces them with forward slashes
            list_of_frames_path.append(image_path)

        new_df = results.pandas()
        new_result = new_df.xywh[0]['name']
        list_of_detected_classes_in_all_frames.append(new_result.tolist())
  # 
  #   for j in range(len(img)):
  #     out.write(img[j])
  #     out.release()


              # image_results = cv2.imwrite(file_name+str(i)+'.jpg',results)
    
    for outer_loop in list_of_detected_classes_in_all_frames:
        for inner_loop in outer_loop:
            if inner_loop:
                detected_classes.append(inner_loop)
    # value_list =[]
    # class_list =[]
    for iterate in detected_classes:
      if iterate not in check_dict:
        check_dict[iterate] = 1
      else:
        check_dict[iterate] =check_dict[iterate]+ 1
          # value_list[len(class_list)-1] += 1
      # value_list.insert(-1,value_list[len(class_list)-1])
      # value_list.pop(len(class_list)-1)
      # class_list.append(iterate)
      # value_list.append(check_dict[iterate])
      # check_dict['class'] = class_list
      # check_dict['value'] = value_list
    # check_dict['imagePath'] = list_of_frames_path
      # check_dict['imagePath'] = path
    
    return check_dict, list_of_frames_path


