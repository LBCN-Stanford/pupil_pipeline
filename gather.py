'''A little tool that gathers all the 'epoched' files into one folder'''
import os
from os.path import join, getsize
from shutil import copy2
def gather(parent, out_dir):

    for root, dirs, files in os.walk(parent):
        for file in files:
            if 'epoched' in file:
                copy2(os.path.join(root, file), out_dir)

if __name__ == '__main__':
    #TODO create new directory
    gather('/home/harrysha/Dropbox/data', 'hi')
