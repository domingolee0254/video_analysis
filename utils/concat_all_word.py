#concat_all_word.py
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
from pororo import Pororo
import re
import json

from correct_result import leven


from correction_phrase import makeJson
'''
# 1. load json file 
- def get_json(json_path)
- json file path -> json file itself

# 2. extract_word in all frame                                                      
- def get_frame(frame_idx, frame_results, file_list):
    - 2-1. frame_results[frame_idx]['frame_result'][ii]['position']를 돌면서 y 좌표만 보기(복음서 이름 y 좌표) 
    - 2-2. frame_results[frame_idx]['frame_result'][ii]['label'][0]['description'] 복음서 이름 바뀌는 프레임 정보(시간, 프레임 이름) 저장
    - 2-3. frame_results[frame_idx]['frame_result'][ii]['position']를 돌면서 y 좌표만 보기(캡션 내용 y 좌표)
    - 2-4. frame_results[frame_idx]['frame_result'][ii]['label'][jj]['description'] 복음서 내용중 각 워드를 한 리스트에 저장

# 2. 한 동영상당 분할된 이미지 로드 
- def getImage(frame_idx)-> image

Good.
Jal doem
# 3. 모든 동영상(10개) 단위로 돌 수 있게 함수화 
'''
# input: json file path
# output: json file
def get_json(json_path):
   with open(json_path, 'r') as f:
        json_data = json.load(f)
        return json_data['frame_results']

# input: frame_results dict
# outpu: array of list [ [1,5], [7, 10], ...]
def get_target_frame_indices(frame_results, max_frame:int):

    output_list = []

    # initialize
    frame_str =''
    target_str = ''
    first_frame_idx = None

    # get caption address
    for frame_idx in range(max_frame):
        #print(f"frame_idx: {frame_idx}")
        has_caption = False
        # get single frame's caption address(e.g., 느헤미야, 창세기, ..., etc.)
        frame_data = frame_results[frame_idx]['frame_result'] 
        for detected_str_idx in range(len(frame_data)):
            
            if (frame_data[detected_str_idx]['position']['y'] == 510) and (frame_data[detected_str_idx]['position']['x'] < 100):
                frame_str = frame_data[detected_str_idx]['label'][0]['description']
                has_caption = True
                #print(f"frame_idx {frame_idx} has caption {frame_str}")
                if first_frame_idx == None:
                    first_frame_idx = frame_idx
                    target_str = frame_str
                    scene_first_time_stamp = frame_results[frame_idx]['timestamp']
                   # print(f"frame_str: {frame_str} \t first_frame_idx: {first_frame_idx} when {scene_first_time_stamp}")
            #print(f"test_2 is {frame_data[detected_str_idx]} \t label is {frame_str}")
        
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
    print(output_list)
    return output_list #[223, 235, '느헤미야', '0:03:44']
        #prior_frame_str = target_str
        # caption_addr = frame_data

def gathering_caption(frame_results, max_frame_idx, frame_list):
    #print(f'here frame_list is {frame_list}')
     #frame_arr is ndarray
    time_tmp_list = []
    char_gather_list = []
    for time_i in frame_list:
        time_tmp_list.append(time_i[-1])  #[00:03:14]
    
    
    for frame_idx in range(max_frame_idx):
        frame_data_time = frame_results[frame_idx]['timestamp']
        #print(frame_data_time)
        
        for time_idx in time_tmp_list:
            #print(f"time_stamp is {time_idx}")
            if frame_data_time == time_idx:
                frame_data_concat = frame_results[frame_idx]['frame_result']
                char_tmp = []
                char_first_row = []
                char_second_row = []
                cnt = 0
                for detected_str_idx in range(len(frame_data_concat)):
                    if (frame_data_concat[detected_str_idx]['position']['y'] > 550) and (frame_data_concat[detected_str_idx]['position']['x'] < 1000):
                        cnt+=1
                        each_word_content = frame_data_concat[detected_str_idx]['label'][0]['description']

                        if frame_data_concat[detected_str_idx]['position']['y'] < 600:
                            char_first_row.append(each_word_content)
                        else:
                            char_second_row.append(each_word_content)
                        #print(f"cor {frame_data_concat[detected_str_idx]['position']} \t cnt is {cnt} \t string is {each_word_content}")
                        #print(each_word_content)
                        #char_tmp.append(each_word_content)
                        #print(f"char_tmp is {char_tmp}")
                #char_tmp = " ".join(char_tmp)
                char_first_row = " ".join(char_first_row)
                char_second_row = " ".join(char_second_row)
                char_gather_list.append(char_first_row + char_second_row)
    time_content_dict = dict(zip(time_tmp_list, char_gather_list))
    print(f"time_content_dict is {time_content_dict}")
    return time_content_dict





def correctionPhrase(frame_list:list):
    # The bible DB '/home/video_anlay/data/db/'
    bibleDBPath = "../data/db/"

    # frame[0] starting frame number
    # frame[1] ending frame number
    # frame[2] book name
    # frame[3] starting time of the caption in video
    # frame[4] content(phrase)

    # get book list
    for _, _, book_list in os.walk(bibleDBPath):
        pass

    print(f"DEBUGGING book_list:{book_list}")
    for frame in frame_list:
        book_name = frame[2]
        isBook = True if book_name+'.txt' in book_list else False
        #assert book_name+'.txt' in book_list, f"ERROR: No book_name {book_name}.txt"
        print(f"{book_name} isBook: {isBook}")

        if isBook:
            book_path = os.path.join(bibleDBPath, book_name+'.txt')
            with open(book_path, 'r', encoding='euc-kr') as f:
                # calculate Leven. distance to figure out the correct text(content or phrase)
                leven_results = np.array([leven(frame[4], line.strip()[5:]) for line in f])
                min_leven_value = np.min(leven_results)
                idx_of_min = np.argmin(leven_results)
                print(f"leven_dis_min: {min_leven_value}")
                print(f"idx_of_min: {idx_of_min}")

                # reset file pointer
                f.seek(0)
                gt_lines = f.readlines()
                print(f"ocr_predicted: {frame[4]} \nDB_gt_line: {gt_lines[idx_of_min][5:]}\n\n")
                frame[4] = gt_lines[idx_of_min][5:]
        else:
            pass

    print(frame_list)
        # (temp) w/o book name correction
        #book_path = os.path.join(bibleDBPath, book_name+'.txt')
        #with open(book_path) as f:
        #    print(f.readline())






def main(target_image_dir):
    file_list = []
    # initial_count = 0
    # for path in os.listdir(target_image_dir):cd ..
    #     if os.path.isfile(os.path.join(target_image_dir, path)):
    #         initial_count += 1
#    print(initial_count)
    #for frame_idx in range(235):
    max_frame_idx = 2300
    frame_list = get_target_frame_indices(frame_results, max_frame_idx)
    time_content_dict = gathering_caption(frame_results, max_frame_idx, frame_list)
    for i in frame_list:
        for key, value in time_content_dict.items():
            if i[-1]==key:
                i.append(value)                  

    print(f"DEBUGGING start correctionPhrase\n\n")
    correctionPhrase(frame_list)
    print(f"DEBUGGING end correctionPhrase\n\n")
    makeJson(frame_list)
    
    # for i in frame_list:
    #     bible_title = frame_list[-2]
    #query_to_key(frame_results, max_frame_idx, frame_list)
    
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