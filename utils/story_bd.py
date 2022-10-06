#easy_ocr ouput visualize
import numpy as np
import cv2
import random
import matplotlib.pyplot as plt
from PIL import ImageFont, ImageDraw, Image
import json
import os
'''

# 1. 제이슨을 불러오기 
def getJson(json_path)->
전체 돌면서 y축 좌표만 보기 

# 2. 한 동영상당 분할된 이미지 로드 
def getImage(frame_idx)-> image

# 3. 제이슨의 label, position, timestamp (or frame_num) 이미지에 overlap

# 4. 모든 동영상(10개) 단위로 돌 수 있게 함수화 
'''

# input: json file path
# output: json file
def getJson(json_path):
   with open(json_path, 'r') as f:
        json_data = json.load(f)
        return json_data['frame_results']

def get_Image_file(frame_idx, frame_results, file_list):
    frame_path_org1 = frame_results[frame_idx]['frame_result']
    for ii in range(len(frame_path_org1)):
        if frame_results[frame_idx]['frame_result'][ii]['position']['y'] > 500:
            file_list.append(frame_results[frame_idx]['frame_url'])
    res = []
    [res.append(x) for x in file_list if x not in res]
    return res    

def find_y(res):
    #find index of last lash '/' and return image name
    file_list = []
    for f_name in res:
        for idx, char in enumerate(reversed(f_name)):
            if char == '/':
                img_name = f_name[-idx:-3]+'png'
                file_list.append(img_name)
                break
    return file_list

def save_key_frame(file_list):
   #get image from my directory   
    for f_name in file_list:
        img_path = os.path.join(*work_dir, 'image_0612_1fps', f_name)
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.imsave(saved_images+'frame_'+str(f_name), img)
     
# globaly used directory
work_dir = ['/home','text_recog','video_analy', '220612']
saved_images = '/home/text_recog/video_analy/saved_images/test/'
target_image_dir = '/home/text_recog/video_analy/220612/image_0612_1fps'

# 1. 제이슨 이름 불러오기
json_file_name = 'result.json'
json_path = os.path.join(*work_dir,json_file_name)
frame_results = getJson(json_path)
file_list = []

def main(target_image_dir):
    initial_count = 0
    for path in os.listdir(target_image_dir):
        if os.path.isfile(os.path.join(target_image_dir, path)):
            initial_count += 1
            #print(initial_count)
        for frame_idx in range(initial_count):
            res = get_Image_file(frame_idx, frame_results, file_list)
        img_name = find_y(res)
        save_key_frame(img_name)
    
if __name__ == "__main__":
    main(target_image_dir)
