"""
Classes to help create events files in python
These may be useful in creating the behavioral data file if
you collected your data in python instead of MATLAB
"""

import scipy.io as spio

class category:
    def __init__(self, name):
        self.name = name
        self.start = []

class events: 
    def __init__(self, data):
        conds = ['ITI', 'Neg', 'Pos', 'Neut']
        self.categories = [category(name) for name in conds]
        self.first = None # Set this
        
        # Fill self.categories.start with the onset times (use seconds)!
        
fname = 'behavioral.mat'
x = events(['yourdata.txt'])
spio.savemat(fname, {'events':x, 'first':x.first})

## To load it back into python
#x= spio.loadmat(fname, squeeze_me=True, struct_as_record=False)
