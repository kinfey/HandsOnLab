'''

function to unzip a file

'''
import zipfile
import os
import sys
import shutil

def unzip(file_name, path):
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall(path)    

'''

function to zip a file

'''
def zip(file_name, path):   
    with zipfile.ZipFile(file_name, 'w') as zip_ref:
        zip_ref.write(path)
        