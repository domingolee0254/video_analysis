#easy_ocr ouput visualize
from cProfile import label
from sqlite3 import Timestamp
import numpy as np
import cv2
import random
import matplotlib.pyplot as plt
from PIL import ImageFont, ImageDraw, Image
import json
import os
import glob
import argparse

'''
# 1. 제이슨 파일 불러오기 
- def get_json(json_path)
- json file path -> json file itself

# 2. 제이슨 파일 불러오기
- def get_frame(frame_idx, frame_results, file_list):
    - 2-1. 제이슨 파일 frame_results[frame_idx]['frame_result'][ii]['position']를 돌면서 y 좌표만 보기 
    - 2-2. frame_results[frame_idx]['frame_result'][ii]['label'][0]['description'] 복음서 이름 바뀌는 프레임 정보(시간, 프레임 이름) 저장

# 2. 한 동영상당 분할된 이미지 로드 
- def getImage(frame_idx)-> image

# 3. 제이슨의 label, position, timestamp (or frame_num) 이미지에 overlap

# 4. 모든 동영상(10개) 단위로 돌 수 있게 함수화 
'''
# input: json file path
# output: json file
def get_json(json_path):
   with open(json_path, 'r') as f:
        json_data = json.load(f)
        return json_data['frame_results']

# input: json file path
# output: json file
# input: json file
# outpu: array of list [ [1,5], [7, 10], ...]
def get_target_frame_indices(frame_results, max_frame:int):

    output_list = []

    # initialize
    frame_str =''
    target_str = ''
    first_frame_idx = None


    for frame_idx in range(max_frame):
        print(f"frame_idx: {frame_idx}")
        has_caption = False
        # get single frame's caption address(e.g., 느혜미야, 창세기, ..., etc.)
        frame_data = frame_results[frame_idx]['frame_result'] 
        for detected_str_idx in range(len(frame_data)):
            if (frame_data[detected_str_idx]['position']['y'] == 510) and (frame_data[detected_str_idx]['position']['x'] < 100):
                frame_str = frame_data[detected_str_idx]['label'][0]['description']
                has_caption = True
                print(f"frame_idx {frame_idx} has caption {frame_str}")
                if first_frame_idx == None:
                    first_frame_idx = frame_idx
                    target_str = frame_str
                    scene_first_time_stamp = frame_results[frame_idx]['timestamp']
                    print(f"frame_str: {frame_str} \t first_frame_idx: {first_frame_idx} when {scene_first_time_stamp}")

        
        # caption -> no caption
        if has_caption is False and first_frame_idx is not None:
            output_list.append([first_frame_idx, frame_idx, frame_str, scene_first_time_stamp])
            first_frame_idx = None
            continue
            #print(output_list)

        # caption A -> caption B
        #    output_list.append([first_frame_idx, frame_idx])
        #    first_frame_idx = None
        #    continue
    output_list_tmp = [[]]
    for for_escape in output_list:
        

        return output_list
        #prior_frame_str = target_str
        # caption_addr = frame_data

def get_frame(frame_idx, frame_results, file_list):
    frame_path_org1 = frame_results[frame_idx]['frame_result']   # 한 프레임 끝
    tmp_str=''
    for ii in range(len(frame_path_org1)): #한 프레임(frame_idx) 안에서 여러개의 디텍션된 문자 영역(ii)
        if frame_results[frame_idx]['frame_result'][ii]['position']['y'] > 509 and frame_results[frame_idx]['frame_result'][ii]['position']['y'] < 511 and frame_results[frame_idx]['frame_result'][ii]['position']['x'] < 100:
            file_list.append(frame_results[frame_idx]['frame_url'])
            if tmp_str == frame_results[frame_idx]['frame_result'][ii]['label'][0]['description']:
                pass
            
            else: #if two des is same => true 
                print(tmp_str)
                print(frame_results[frame_idx]['frame_result'][ii]['label'][0]['description'])
                tmp_str = frame_results[frame_idx]['frame_result'][ii]['label'][0]['description']
                print(tmp_str)
    res = []
    [res.append(x) for x in file_list if x not in res]
    #print(res)
    return res    

# def find_y(res):
#     #find index of last lash '/' and return image name
#     file_list = []
#     for f_name in res:
#         for idx, char in enumerate(reversed(f_name)):
#             if char == '/':
#                 img_name = f_name[-idx:-3]+'png'
#                 file_list.append(img_name)
#                 break
#     print(file_list)
#     return file_list

# def save_key_frame(file_list):
#    #get image from my directory   
#     for f_name in file_list:
#         img_path = os.path.join(*work_dir, 'image_0612_1fps', f_name)
#         img = cv2.imread(img_path)
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         plt.imsave(saved_images+'frame_'+str(f_name), img)
     

def main(target_image_dir):
    file_list = []
    # initial_count = 0
    # for path in os.listdir(target_image_dir):cd ..
    #     if os.path.isfile(os.path.join(target_image_dir, path)):
    #         initial_count += 1
#    print(initial_count)
    #for frame_idx in range(235):
    max_frame_idx = 2310
    frame_list = get_target_frame_indices(frame_results, max_frame_idx)
    print(frame_list)
        #res = get_frame(frame_idx, frame_results, file_list)
    #print(res)
    #get_segment(res)
    #img_name = find_y(res)
    #save_key_frame(img_name)
    
if __name__ == "__main__":
    #parser = argparse.ArgumentParser(description='Argparse Tutorial')    
    #parser.add_argument('--path', type=str, default=None)
    #args = parser.parse_args()    
    #print(f"path_input: {args.path}")
    # globaly used directory
    work_dir = ['/home','video_analy', '220612']
    saved_images = '/home/video_analy/220612/220612_key_frame_0731/'
    target_image_dir = '/home/video_anlay/220612/image_0612_1fps/'

    # 1. 제이슨 이름 불러오기
    json_file_name = 'result.json'
    json_path = os.path.join(*work_dir,json_file_name)
    frame_results = get_json(json_path)
    
    main(target_image_dir)