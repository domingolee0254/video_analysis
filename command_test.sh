#!/bin/bash
 
PWD=$(pwd)
echo $PWD

VAR=$(ls */)
echo $VAR

for var in $VAR
do
  #echo $PWD/$var
  python path_test.py --path $var
done