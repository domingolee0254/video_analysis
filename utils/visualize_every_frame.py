#easy_ocr ouput visualize
from re import A
import numpy as np
import cv2
import random
import matplotlib.pyplot as plt
from PIL import ImageFont, ImageDraw, Image
import json
import os
'''
#대상 데이터 파일 = 0612_sample.mp4

# 1. 제이슨을 불러오기 
def getJson(json_path)->
- 시간에 해당하는 부분만 제이슨 로드  

# 2. 한 동영상당 분할된 이미지 로드 
def getImage(frame_idx)-> image
- 분할된 이미지와 제이슨에서 프레임 넘버에 맞추기 


# 3. 제이슨의 label, position, timestamp (or frame_num) 이미지에 overlap

# 4. 모든 동영상(10개) 단위로 돌 수 있게 함수화 
'''

# input: json file path
# output: json file
def getJson(json_path):
   with open(json_path, 'r') as f:
        json_data = json.load(f)
        #print(json_data['frame_results'])
        return json_data['frame_results']

def loadImage(frame_idx, frame_results):
    frame_num_per_sec = frame_results[frame_idx]['frame_number']
    #print(f'frame_num_per_sec: {frame_num_per_sec}')
    cnt=1
    for idx in range(60):
        frame_id = 60*(frame_idx)+cnt
        img_path = os.path.join(*work_dir, 'image_0612_60fps', str(frame_id)+'.jpg')
        #print(img_path)
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #print(f"img shape: {img.shape}")    
        img = Image.fromarray(img)
        font = ImageFont.truetype('/home/text_recog/ko_font/HMKMRHD.TTF', 20)    
        draw = ImageDraw.Draw(img)
        np.random.seed(100)
        COLORS = np.random.randint(0, 255, size=(255, 3),dtype="uint8")
        #print(frame_idx)
        frame_infos = frame_results[frame_idx]['frame_result'] # 'label', 'position'   frame_idx=0
        for frame_info in frame_infos:
            label_info = frame_info['label'][0]['description']
            position_info = list (frame_info['position'].values() )
            #print(label_info, len(label_info))
            #print(position_info)
            x = position_info[0]
            y = position_info[1]
            w = position_info[2]
            h = position_info[3]
            #print(x, y, w, h)
            #color_idx = random.randint(0,255) 
            #color = [int(c) for c in COLORS[color_idx]]
            #color = [0,102,153]
            color = [255,0,0]
            draw.rectangle(((x, y), (x+w, y+h)), outline=tuple(color), width=2)
            #print(f'text: {label_info}')
            draw.text((x+10,y-30), label_info, font=font, fill=tuple(color), align='left')    
        numpy_image=np.array(img)  
        img = cv2.cvtColor(numpy_image, cv2.COLOR_BGR2RGB)
        cv2.imwrite(saved_images+'frame_'+str(frame_id)+'.jpg', img)

        cnt+=1

# globaly used directory
work_dir = ['/home','text_recog','video_analy','0612']
saved_images = '/home/text_recog/video_analy/saved_images/2022-06-12_fps60_hy/'


# 1. 제이슨 이름 불러오기
json_file_name = 'request_res_0612_sample_hy.json'
json_path = os.path.join(*work_dir,json_file_name)
frame_results = getJson(json_path)

initial_count = 0
target_image_dir = '/home/text_recog/video_analy/0612/image_0612_60fps/'
for path in os.listdir(target_image_dir):
    target_images_path = os.path.join(target_image_dir, path)
    initial_count += 1
    #print(target_images_path)
#for frame_idx in range(initial_count+2):
for frame_idx in range(244):
    loadImage(frame_idx, frame_results)
