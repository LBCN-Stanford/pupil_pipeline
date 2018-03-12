import os
import numpy as np
from timeit import default_timer as timer
from misc import make_path
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt


def plot_raw(raw, name='raw_plot', title='Raw Data Plot', out_dir='', base_name='', **params):
    '''
    Creates a scatter plot from the raw data and saves it to a file.
    Takes in the dataframe and requires params['out_dir'], and params['base_name']
    '''
    ax = raw.plot(x='Time', y='Pupil', kind='scatter', title=title)
    ax.set(xlabel="Time", ylabel="Pupil Diameter (mm)")
    plt.savefig(make_path(name, '.png', out_dir=out_dir,
                          base_name=base_name, **params))
    plt.cla()
    plt.clf()
    plt.close()


def check_outliers(raw, impossible_upper=5, impossible_lower=1.5, out_dir='', base_name='', **params):
    '''
    Counts and removes outliers in the raw data. Saves a report of the number
    of unusable samples based on the largest and smallest values specified in
    params['impossible_upper'] and params['impossible_lower'].
    '''

    nsamples = len(raw)

    raw.loc[(raw.Pupil < impossible_lower) | (
        raw.Pupil > impossible_upper), 'Pupil'] = np.nan
    count = raw.Pupil.count()
    string = '{} out of {} samples were within acceptable range({} - {})\nPercentage of usable data: {}%'.format(
        count, nsamples, impossible_lower, impossible_upper, count / nsamples * 100)
    print(string)
    with open(make_path('outlier_report', '.txt', base_name=base_name, out_dir=out_dir, **params), 'w') as f:
        f.write(string)


def calculate_stats(raw, fname='descriptive_stats', plot=True, out_dir='', base_name='', **params):
    '''
    Calculates descriptive statistics on the raw data. Save the results into a
    file called descriptive_stats. Another plot with these stats is saved in
    a file called raw_plot_with_stats_outliers_removed.
    '''
    stats = raw.Pupil.describe()
    if plot:
        ax = raw.plot(x='Time', y='Pupil', kind='scatter',
                      title='Raw Data (Outliers Removed)')
        plt.axhline(stats['mean'], color='r', label='mean')
        plt.axhline(stats['25%'], color='g', label='25%')
        plt.axhline(stats['50%'], color='g', label='median')
        plt.axhline(stats['75%'], color='g', label='75%')
        ax.set(xlabel="Time", ylabel="Pupil Diameter (mm)")
        plt.legend()
        plt.savefig(make_path('raw_plot_with_stats_outliers_removed', '.png',
                              out_dir=out_dir, base_name=base_name))
        plt.cla()
        plt.clf()
        plt.close()
    stats.to_csv(
        make_path(fname, '.csv', out_dir=out_dir, base_name=base_name))


def qualitycheck(raw, out_dir='', base_name='', **params):
    '''
    Does a quality check of the raw data. Using paramters in **params.
    '''
    print('\nChecking the quality...\n')
    plot_raw(raw, out_dir=out_dir, base_name=base_name)
    check_outliers(raw, out_dir=out_dir, base_name=base_name)
    calculate_stats(raw, out_dir=out_dir, base_name=base_name)
    raw.to_csv(make_path('outliers_removed', '.csv', out_dir=out_dir,
                         base_name=base_name), index=False)
