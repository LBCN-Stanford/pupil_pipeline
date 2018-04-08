'''
A little tool that gathers all the 'epoched' files into one folder
Run the program like this python gather.py searchfolder
It will look through all the subfolders of the searchfolder and then copy
the *epoched*pkl files in a folder in the search folder called 'Gathered' 
'''
import os
from shutil import copy2
import sys

def gather(parent, out_dir):
    for root, dirs, files in os.walk(parent):
        for file in files:
            if 'epoched' in file and 'pkl' in file:
                if not os.path.exists(os.path.join(out_dir, file)):
                    copy2(os.path.join(root, file), out_dir)

if __name__ == '__main__':
    assert (len(sys.argv) == 2), 'Please run the code like this: python gather.py searchfolder'
    parent = sys.argv[1]
    child = os.path.join(parent, 'Gathered')
    if not os.path.isdir(child):
        os.makedirs(child)
    gather(parent, child)
