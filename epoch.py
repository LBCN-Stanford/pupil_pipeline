import scipy.io as spio
import numpy as np
from readpupil import read_pupil
from misc import make_path, save_pkl, select_files
import sys
import warnings
from params import get_params
import os


def read_events(fname, p_first):
    ''' Reads and aligns the events file.
    Arguments:
        fname: which should be a .mat file of the events
                format (see tutorial)
        p_first: Time of the first pupil event. (ms)

    Returns:
        categories: list of rows of a MATLAB struct
                    array (see tutorial)

    '''
    matfile = spio.loadmat(fname, squeeze_me=True, struct_as_record=False)
    try:
        events = matfile['events']
        first = matfile['first']
    except KeyError:
        print('Make sure your events file has a struct called events,',
              'and a float called first!')
        sys.exit()

    categories = events.categories
    # Convert values in events data to milliseconds and align
    for category in categories:
        category.start = 1000 * category.start + p_first - first * 1000
    return categories


def time_to_samples(time, sample_rate=250):
    return int(sample_rate * time / 1000)


def get_nsamples(sample_rate=250, epoch_time=200, back_time=60, **params):
    '''Returns the number of samples to epoch given the sample_rate
    and epoch time in milliseconds.
    '''
    # TODO: Replace
    return (int(sample_rate * back_time / 1000),
            int(sample_rate * epoch_time / 1000))


def get_nearest_ind(pupil_events, time, threshold=20):
    '''Finds the pupil event with the nearest start time to time'''
    difference = np.abs(pupil_events.Time - time)
    # if difference.min() > threshold:
    #     print('WARNING the nearest index in the pupil data to your event '\
    #         'was {} away from you event, which is larger than'\
    #         'your threshold, {}. Please check alignment.'.format(difference.min(), threshold))
    return difference.argmin()


class Epoched:
    """ An object that stored information about the epoched data
    Attributes:
        matrix: (n_categs x n_samples x n_trials) of pupil
                diameter data. First dimension is the condition
                second is the 'time' and third is the trial
        names: a list of names of conditions
        num_rejected: a list of numbers of rejected trials for each condition
        num_trials: a list of number of number of trials in each condition
        n_categs: number of categories
        n_forwardsamples: number of samples forward
        n_backsamples: number of samples before onset
        total_samples: total number of samples per epoch
    """

    def __init__(self, n_categs, n_samples, n_trials):
        self.total_samples = n_samples[0] + n_samples[1]
        self.matrix = np.empty((n_categs, self.total_samples, n_trials))
        self.matrix[:] = np.nan
        self.n_categs, self.n_forwardsamples, self.n_backsamples = n_categs, n_samples[
            1], n_samples[0]
        self.names, self.num_trials, self.num_rejected = [], [], []
        self.rejected = {}



def get_baseline(pupil_data, onset, baseline_type='no', sample_rate=250, bl_events=None):
    if baseline_type == 'no':
        return 0
    elif type(baseline_type) == int:
        bl_samples = time_to_samples(baseline_type, sample_rate)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return np.nanmean(pupil_data.Pupil.iloc[onset - bl_samples - 1:onset - 1].values)
    else:
        difference = bl_events.Time - pupil_data.Time.iat[onset]
        difference = difference[difference <= 0]
        if len(difference) == 0:
            return np.nan
        bl_ind = difference.argmax()
        bl_samples = time_to_samples(baseline_type[2], sample_rate)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return np.nanmean(pupil_data.Pupil.iloc[bl_ind + 1: bl_ind + bl_samples + 1].values)


def get_baseline_events(pupil_events, category):
    onsets = list(map(lambda x: get_nearest_ind(
        pupil_events, x), category.start))
    return pupil_events.loc[onsets]


def epoch(pupil_data, events_path, sample_rate=250, epoch_time=200,
          back_time=60, out_dir='', base_name='', baseline_type='no', **params):
    '''
    Epochs the pupil_data according to behavioural events specified
    by the events file in events_path.

    Parameters:
        pupil_data: A pupil_data object like the one loaded by read_pupil
        events_path: A path to the events file (see tutorial)
        sample_rate: The sample rate of your pupil recording
        epoch_time: Time in ms to epoch
        back_time: Time before the event to plot

    Returns:
        epoched: an Epoched object defined above
    '''

    print('\nEpoching...\n')

    # Find all the events
    pupil_events = pupil_data[pupil_data['Content'] != '-']
    num_events = len(pupil_events)
    print('There are {} events in the pupil data, does '
          'this look correct? If not, the first two events '
          'of pupil may not have been recorded...'.format(num_events))

    # Reads behavioral events
    # TODO: from python
    categories = read_events(events_path, pupil_events.Time.iat[0])
    samples_per_epoch = get_nsamples(sample_rate, epoch_time, back_time)
    # Initialize output variables
    epoched = Epoched(len(categories), samples_per_epoch, num_events)
    # Extra: Report median miss time.
    # Get the baseline dictionary mapping from time to baseline values.
    bl_events = None
    if type(baseline_type) == tuple:
        bl_events = get_baseline_events(
            pupil_events, categories[baseline_type[1]])

    for c, category in enumerate(categories):
        epoched.names.append(category.name)
        # +1 to exclude the content sample, which is out of sync.
        onsets = list(map(lambda x: get_nearest_ind(
            pupil_events, x) + 1, category.start))
        rejected_inds = []
        rejected = 0
        for t, onset in enumerate(onsets):
            # Note the -1 to avoid the content sample
            pre = pupil_data.Pupil.iloc[onset -
                                        samples_per_epoch[0] - 1: onset - 1].values
            post = pupil_data.Pupil.iloc[onset:onset +
                                         samples_per_epoch[1]].values
            baseline = get_baseline(
                pupil_data, onset, baseline_type, sample_rate, bl_events)
            trial = np.concatenate((pre, post)) - baseline

            if np.isnan(np.sum(trial)): # Checks if there is a nan
                rejected_inds.append(t)
                rejected += 1
            elif len(trial) == sum(samples_per_epoch):
                epoched.matrix[c, :, t - rejected] = trial

        epoched.num_trials.append(len(onsets))
        epoched.num_rejected.append(rejected)
        epoched.rejected[category.name] = rejected_inds

    # Save .mat and .pkl of epoched data
    spio.savemat(make_path('epoched', '.mat', out_dir=out_dir,
                           base_name=base_name), {'epoched': epoched})
    save_pkl(make_path('epoched', '.pkl', out_dir=out_dir,
                       base_name=base_name), epoched)

    return epoched


# Testing purposes
if __name__ == '__main__':
    pupil_path = select_files('preprocessed pupil file')[0]
    pupil_data = read_pupil(pupil_path)
    events_path = select_files('events file: ')[0]
    params = get_params(sys.argv)
    params['out_dir'] = os.path.dirname(pupil_path)
    epoch(pupil_data, events_path, **params)
