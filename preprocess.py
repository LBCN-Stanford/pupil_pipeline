import numpy as np
from scipy import interpolate
from qualitycheck import calculate_stats
from misc import make_path

def make_blink_list(pupil_data):
    '''
    Takes in the pupil_data dataframe and returns a list of tuples of the following
    form: (last sample before blink, first sample after blink)
    '''
    blink_list = []
    nans = pupil_data[np.isnan(pupil_data.Pupil)]

    start = None
    for j, i in enumerate(nans.index.values):
        if start == None: start = i
        if j + 1 == len(nans.index.values): break
        if i + 1 != nans.index.values[j + 1]: # If the next index was not a nan
            blink_list.append((start - 1, i + 1))
            start = None

    return blink_list


def interpolate_blinks(pupil_data, min_blink_time=20, max_blink_time=500, sample_rate=250, **params):
    '''
    Interpolates blinks, which are defined as a sequence of 0s that lasts for a time
    between min_blink_time, and max_blink_time. Sequences of 0s that are shorter than
    min_blink_time are front-filled, and sequences that are longer than max_blink_time
    are ignored.

    Arguments:
        pupil_data: A pupil_data dataframe like the one read in by read_pupil
        min_blink_time: (ms)
        max_blink_time: (ms)
        sample_rate: (hz)


    '''
    blink_list = make_blink_list(pupil_data)
    min_blink = int(min_blink_time * sample_rate / 1000)
    max_blink = int(max_blink_time * sample_rate / 1000)

    for i2, i3 in blink_list: # For each blink...
        blink_len = i3-i2-1
        if blink_len < min_blink: # If too short for a blink just front fill
            pupil_data.loc[np.arange(i2 + 1, i3, 1), 'Pupil'] = pupil_data.Pupil.iat[i2]
        elif blink_len < max_blink: # Interpolate blinks...
            i1, i4 = 2 * i2 - i3, 2 * i3 - i2
            indices = [i1, i2, i3, i4]
            if i1 > 0 and i4 < len(pupil_data): # ...if its in range...
                samples = list(map(lambda x: pupil_data.Pupil.iat[x], indices))
                tck = interpolate.splrep(indices, samples)
                i_new = np.arange(i2 + 1, i3, 1)
                pupil_data.loc[i_new, 'Pupil'] = interpolate.splev(i_new, tck)



def preprocess(pupil_data, out_dir='', base_name='', **params):
    '''
    Interpolates blinks, and sets the start of the pupil recording to 0.
    Saves files.
    Arguments:
        pupil_data: Dataframe like the one read in by read_pupil
        out_dir: Outputs will be saved to this directory
        base_name: String is appended to output files
    '''

    print('\nPreprocessing...\n')
    interpolate_blinks(pupil_data, **params)
    calculate_stats(pupil_data, fname='descriptive_stats_post_preprocessing',
                    plot=False, out_dir=out_dir, base_name=base_name)

    t0=pupil_data.Time.iloc[0]
    pupil_data['Time'] = pupil_data.Time.apply(lambda x: x - t0)
    pupil_data.to_csv(make_path('preprocessed', '.csv', out_dir=out_dir,
                        base_name=base_name), index=False)
