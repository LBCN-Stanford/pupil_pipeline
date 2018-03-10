# import numpy as np
from misc import load_pkl, make_path
import pandas as pd
from params import get_params
import sys
import json
import tkinter as tk
from tkinter import filedialog
import pickle
from epoch import Epoched

with open('epoched.pkl', 'rb') as f:
	x= pickle.load(f)

print(99)
