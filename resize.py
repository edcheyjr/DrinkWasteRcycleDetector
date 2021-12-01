# imports
from PIL import Image
from natsort import natsorted
import glob
import os
from moviepy.editor import *
import cv2

# for testing
# Directory
img_directory = "Images"
  
# Parent Directory path
parent_dir = "/Users/edwin/Documents/WasteClassfication/yolov5/DrinkWasteWebDemo/backend/"
  
# Path
image_path = os.path.join(parent_dir, img_directory)

#  calculate aspect ratio
def aspect_ratio_cal(width, height ,org_width, org_height, aspect_ratio = False):
   
    if org_width > org_height and aspect_ratio is True:
        AR = org_height / org_width
        new_height = width *AR
        new_width = width
    elif org_width < org_height and aspect_ratio is True:
        AR = org_width / org_height
        new_width = height *AR 
        new_height = height
    elif org_width == org_height and aspect_ratio is True:
        AR = 1
        new_width = height *AR
        new_height = height
    else:
        new_width = width   
        new_height = height
    return new_width, new_height



# image resize
def image_resize(imgPath, resizePath, width, height, mantain_aspect_ratio = None):
# declare list to store images before and after resize
    image_list = []
    resized_image = []
    
#    store images in an array 
    for filename in natsorted(glob.glob(imgPath)):
        print(filename) 
        img = Image.open(filename)
        image_size = img.size
        image_list.append(img)
        image_list = image_list[:10]
        
#         get image name, size and format
    # filename_array = filename.split("/")
    # image_name_with_ext = filename_array[-1]
    # refactor to use os instead
    image_name_with_ext = os.path.basename(filename)

    print(image_name_with_ext)

    # refactor with os
    # image_name_arr = image_name_with_ext.split('.')

    # image_name = image_name_arr[0]
    # image_format = image_name_arr[1]
    image_name =os.path.splitext(image_name_with_ext)[0]
    image_format = os.path.splitext(image_name_with_ext)[1]
    (image_width, image_height)=  image_size
    
#     print Image info
    print('\n\n====================================')
    print(' IMAGE INFO:')
    print('image size {}'.format(image_size))
    print('image_width{}'.format(image_width))
    print('image height {}'.format(image_height))
    print('image name {}'.format(image_name))
    print('image format {}'.format(image_format))
    print('==================================== \n\n')


#     mantaining aspect ratio
    new_width, new_height = aspect_ratio_cal(width, height, image_width, image_height, mantain_aspect_ratio)
    
#     resize images

    for image in image_list:
#         image.show()
        resized_img = image.resize((int(new_width), int(new_height)))
        resized_image.append(resized_img)
         
#     save images into a folder which will be used by detect 
    for rsz_img in resized_image:
        print(rsz_img)
        # rsz_img.show()
        if(image_format.lower() =='png' or 'jpeg'or 'jpg'):
            rsz_img.save('{}{}{}{}'.format(resizePath,image_name,'_resized.',image_format))  
        else:
            print("Error: Could not find that image format")
# clear reized image array
    resized_image.clear()  

 
# video resize

# video resize
# resizes the video
def video_resize(input_file_path, resized_vid_file_path, width, height,maintain_aspect_ratio=None):
    clip = VideoFileClip(input_file_path)

#  orginal video clip details 
    org_vcap = cv2.VideoCapture(input_file_path) # 0=camera
    # height and width of the video clip
    org_height = clip.h
    org_width =clip.w

    # fps
    
    if org_vcap.isOpened():
        org_fps = org_vcap.get(5) # float `fps`    
    print('\n\n ==================================== ')
    print('        VIDEO INFO:        ')
    print('\n')
    print('video height {} and width {} and fps {}'.format(org_height,org_width,org_fps))

    # aspect ratio 
    new_width, new_height = aspect_ratio_cal(width,height,org_width,org_height,maintain_aspect_ratio)

    print('new width {} and height {}'.format(new_width,new_height))

    clip_resized = clip.resize(height=new_height) # make the height 360px ( According to moviePy documenation The width is then computed so that the width/height ratio is conserved.)


    # video details
    # height and width of the video clip
    height = clip_resized.h
    width =clip_resized.w

    # img = cv2.imread('my_image.jpg',0)

    clip_resized.write_videofile(resized_vid_file_path)


    vcap = cv2.VideoCapture(resized_vid_file_path) # 0=camera
 
    if vcap.isOpened(): 
    #     # get vcap property 
    #     # width  = vcap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)   # float `width`
    #     # height = vcap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)  # float `height`
    #     # or
    #     width  = vcap.get(3)  # float `width`
    #     height = vcap.get(4)  # float `height`

        # it gives me 0.0 :/
        fps = vcap.get(5)  # float `fps`

        # fps = vcap.get(cv2.cv.CV_CAP_PROP_FPS)
    print('after resizing')    
    print('video height {} and width {} and fps {}'.format(height,width,fps))
    print('==================================== \n\n')
    

    # return clip_resized