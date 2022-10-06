'''
tf-idf.py
author: pancho
date: Aug.17.22
'''
from cgitb import reset
from sklearn.feature_extraction.text import TfidfVectorizer
from pandas import DataFrame
import pandas as pd
from math import log 
import numpy as np
import os

def ReadTextFile(file_list):  
  for file_name in file_list:
    f = open(file_name, 'r', encoding='utf-8')
    script_tmp_list = []
    while True:
      line = f.readline()
      line = line.strip()
      script_tmp_list.append(line)
      if not line: break
      tmp_char = " ".join(script_tmp_list)
    corpus.append(tmp_char)
  f.close()
  return corpus

def TFIDF(corpus):

  tfidfv = TfidfVectorizer().fit(corpus)
  tfidfv_arr = tfidfv.transform(corpus).toarray()
  tfidfv_dict = tfidfv.vocabulary_
  keyword_list = []
  
  for doc_arr in tfidfv_arr:
    topid = sorted(range(len(doc_arr)),key= lambda i: doc_arr[i])[-10:]  #[123,13,31314,512]
    keyword_list_per_row = []
    for topid_ in topid:
      for key, value in tfidfv_dict.items():
        if topid_ == value:
          keyword_list_per_row.append(key)
    keyword_list.append(keyword_list_per_row)
  
  for idx,keyword in enumerate(keyword_list):
    print(f"keyword_{idx}th_docs are {keyword}\n")

def main(root_dir):
  file_tmp_list = os.listdir(root_dir) #['json', '2022-06-12.txt', 'src_video', 'db', '2021-02-21.txt']
  for file_name in file_tmp_list:
    f_name = os.path.join(root_dir, file_name) #/home/video_analy/data/json | /home/video_analy/data/2022-06-12.txt
    if os.path.isfile(f_name) == True: 
      file_list.append(f_name)
     # file_list_txt = [file for file in file_list if file.endswith(".txt")]
  corpus = ReadTextFile(file_list)
  res = TFIDF(corpus)

if __name__=="__main__":
  root_dir = "/home/video_analy/data/script"
  file_list = []
  corpus = []
  main(root_dir)
