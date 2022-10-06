import os
import glob
import re 
import json
from collections import OrderedDict

'''
1. Correction (L_distance)

input : final_frame_list
output: corrected final_frame_list

This module compares string in the input, which is contaminated by some noise,
and the Bible DB, which has correct phrases corresponding to the input string,
and outputs correct string from the Bible DB.
'''
def correctPhrase():
    pass
    return None



'''
2. Make JSON file

input : final_frame_list
output: correct text from DB

This module compares string in the input, which is contaminated by some noise,
and the Bible DB, which has correct phrases corresponding to the input string,
and outputs correct string from the Bible DB.
'''
#
def makeJson(final_frame_list:list):
    print(f"\n\n Building makeJson... \n\n")
    print(f"len(): {len(final_frame_list)} \t final_frame_list: {final_frame_list}")
    # frame[0] starting frame number
    # frame[1] ending frame number
    # frame[2] book name
    # frame[3] starting time of the caption in video
    # frame[4] content(phrase)

    file_data = OrderedDict()

    # meta data
    file_data["title"]    = "untitled"
    file_data["link"]     = "no link"

    content = []
    for frame in final_frame_list:
        content.append({ "time_start": frame[3],
                    "time_end": None,
                    "content": frame[2],
                    "text": frame[4]   })


    file_data["contents"] = content

    with open('output.json', 'w', encoding="utf-8") as make_file:
        json.dump(file_data, make_file, ensure_ascii=False, indent="\t")