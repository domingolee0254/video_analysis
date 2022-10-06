'''
request.py
author: pancho 
date: 220706
'''
import os
import time
import requests
import json
from os import path
from PIL import Image
import os
import sys
import argparse 

# requrest json file of video
# save the result json file(utf-8)
# result_data = json.loads(result_response.content)를 하면 dict 형태로 받는다.
def communicator_video(module_url, video_path, video_text, extract_fps, start_time, end_time, module_type, save_json_path):
    json_video = open(video_path, 'rb')
    json_files = {'video': json_video}
    json_data = dict({
        "analysis_type": module_type,
        "video_text": video_text,
        "extract_fps": extract_fps,
        "start_time": start_time,
        "end_time": end_time
    })
    result_response = requests.post(url=module_url, data=json_data, files=json_files)
    result_data = json.loads(result_response.content)
    #print(f'result_data is: {result_data}')
    #print(f'result_data type is: {result_data.type}')
    result = result_data['result']
    with open(save_json_path+'/220612_gaspel_response.json', 'w', encoding='utf-8') as outfile:
        json.dump(result, outfile)
    return result

# main function
# call communicator_video func
#
def main(module_url, video_path, video_text, extract_fps, start_time, end_time, module_type, save_json_path): 
    result = communicator_video(module_url, video_path, video_text, extract_fps, start_time, end_time, module_type, save_json_path)
    return result

if __name__ == '__main__':
    
    module_url = "http://mllime.sogang.ac.kr:12100/video/" 
    video_path = "/home/video_analy/video/2022-06-12_gaspel.mp4"
    video_text = ""
    extract_fps = 1
    start_time = ""   
    end_time = ""
    module_type = "video"
    save_json_path = '/home/video_analy/220612/' 
    res = main(module_url, video_path, video_text, extract_fps, start_time, end_time, module_type, save_json_path)    
    #print(res)
   
# root_dir = '/home/text_recog/video_analy/video' # root_dir

# video_abs_path_list = []
# possible_img_extension = ['.mp4']

# for (root, dirs, files) in os.walk(root_dir):
#     if len(files) > 0:
#         for file_name in files:
#             if os.path.splitext(file_name)[1] in possible_img_extension:
#                 img_path = root + '/' + file_name
#                 img_path = img_path.replace('\\', '/') # replace \ -> \\
#                 video_abs_path_list.append(img_path)

# for vid in video_abs_path_list:
#     vid
# print(video_abs_path_list)


# def file_load(video_path):
#     os.path.dirname()    
    
    
#     path = video_path
#     file_list = os.listdir(path)
        
#     print ("file_list: {}".format(file_list))
