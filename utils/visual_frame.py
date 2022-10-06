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
        #print(json_data['frame_results'])



def getImage(frame_idx, frame_results):
    frame_path_org = frame_results[frame_idx]['frame_url']
    # find index of last lash '/' and return image name
    for idx, char in enumerate(reversed(frame_path_org)):
        if char == '/':
            img_name = frame_path_org[-idx:-3]+'png'
            break

    # get image from my directory   
    img_path = os.path.join(*work_dir, 'image' ,img_name)
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #print(f"img shape: {img.shape}")    
    img = Image.fromarray(img)
    font = ImageFont.truetype('/home/text_recog/ko_font/HMKMRHD.TTF', 20)    
    draw = ImageDraw.Draw(img)
    
    np.random.seed(100)
    COLORS = np.random.randint(0, 255, size=(255, 3),dtype="uint8")

    frame_infos = frame_results[frame_idx]['frame_result'] # 'label', 'position'
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
        print(f'text: {label_info}')
        draw.text((x+10,y-30), label_info, font=font, fill=tuple(color), align='left')    

    #plt.figure(figsize=(50,50))
    plt.imshow(img)
    #plt.show()
    plt.imsave(saved_images+'frame_'+str(frame_idx)+'.png', img)

# globaly used directory
work_dir = ['/home','text_recog','video_analy']
saved_images = '/home/text_recog/video_analy/saved_images/2022-06-12/'

# 1. 제이슨 이름 불러오기
json_file_name = 'result.json'
json_path = os.path.join(*work_dir,json_file_name)
frame_results = getJson(json_path)

initial_count = 0
target_image_dir = '/home/text_recog/video_analy/image'
for path in os.listdir(target_image_dir):
    if os.path.isfile(os.path.join(target_image_dir, path)):
        initial_count += 1
for frame_idx in range(initial_count+2):
    print(frame_idx)
    getImage(frame_idx, frame_results)

