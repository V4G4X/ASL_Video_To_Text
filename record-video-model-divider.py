import cv2
import numpy as np
import os, shutil
from datetime import datetime

#now = datetime.now()
#timestamp = now.strftime('%Y%m%d_%H%M%S')
#filename = 'video_' + timestamp + '.avi'
frames_per_second = 24.0
res = '480p'
sequence_length = frames_per_second*3

#Set resolution for video capture
def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

# Standard Video Dimensions Sizes
STD_DIMENSIONS =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
}

def get_dims(cap, res='480p'):
    width, height = STD_DIMENSIONS['480p']
    if res in STD_DIMENSIONS:
        width, height = STD_DIMENSIONS[res]
    change_res(cap, width, height)
    return width, height

# Video Encoding, might require additional installs
# Types of Codes: http://www.fourcc.org/codecs.php
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    #'mp4': cv2.VideoWriter_fourcc(*'H264'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}

#Returns video writer for the particular extension
def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
      return VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']


cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print('Cannot access webcam!!')
    exit()

dims = get_dims(cap, res=res)
#video_type_cv2 = get_video_type(filename)

#out = cv2.VideoWriter(filename, video_type_cv2, frames_per_second, dims)

count = 0
X = [] #list to store sequence of images
flag = False 

if os.path.exists(r'LiveRecording') and os.path.isdir(r'LiveRecording'):
    shutil.rmtree(r'LiveRecording')
os.mkdir(r'LiveRecording')

img = cv2.imread('doggo.jpg')
img = cv2.resize(img, (640, 480))

while True:
    frames_list = []
    now = datetime.now()
    timestamp = now.strftime('%Y%m%d_%H%M%S')
    filename = 'video_' + timestamp + '.mp4'
    filename = os.path.join('LiveRecording', filename)
    video_type_cv2 = get_video_type(filename)
    writeVid = cv2.VideoWriter(filename, video_type_cv2, frames_per_second, dims)
    while count < sequence_length:   
        ret, frame = cap.read()
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Recording', frame)
        frames_list.append(frame)
        writeVid.write(frame)
        count += 1
        key = cv2.waitKey(33)
        if key == 10 or key == 13:
            flag = True

    writeVid.release()

    cv2.imshow('Recording',img)
    key = cv2.waitKey(2000)
    if key == 10 or key == 13:
            flag = True

    X.append(frames_list)
    count = 0

    if flag:
        break

print('\n\nLength of X: {}'.format(len(X)))        

cap.release()
#out.release()
cv2.destroyAllWindows()    
