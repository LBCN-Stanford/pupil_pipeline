'''
File that reads in the pupil diameter data
'''
import pandas as pd
import numpy as np

def read_pupil(path):
    """
    Given a path to the pupil diameter data, returns a Dataframe with the
    given info. Inputs may be of .txt, .xlsx, or .csv.
    """
    print('\nLoading in the data...\n')
    tail = path[-4:]
    raw = None
    if tail == '.txt':
        raw = pd.read_csv(path, delimiter='\t')
    elif tail == 'xlsx':
        raw = pd.read_excel(path)
    elif tail == '.csv':
        raw = pd.read_csv(path)
    else:
        raise ValueError('Please select a .txt, .xlsx or .csv file. ')

    raw.columns = ['Time', 'Pupil', 'Content']

    # If the Pupil is not already a numeric type, make it so.
    if not np.issubdtype(raw['Pupil'].dtype, np.number):
        raw.Pupil.replace({'-': np.nan}, inplace=True)
        raw.Pupil = pd.to_numeric(raw.Pupil)
    return raw
