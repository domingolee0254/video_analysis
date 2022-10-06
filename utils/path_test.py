import os 
import argparse

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, help='an integer for printing repeatably', default=None)
    args = parser.parse_args()
    print(f'path is: {args.path}') 