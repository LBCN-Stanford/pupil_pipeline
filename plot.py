import numpy as np
import scipy.stats as stat
from misc import load_pkl, make_path, select_files
from epoch import Epoched
import params
import warnings
import os
import sys
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

def_cols = plt.rcParams['axes.prop_cycle'].by_key()['color']
def_style = ['-' for i in range(10)]


def plot_conds(epoched, conds_to_plot='all', plot_colors=def_cols,
               plot_style=def_style, plot_error=True, sample_rate=250,
               back_time=60, plot_title='Pupil Diameter',
               plot_fname='pupil_diameter_plot',
               out_dir='', base_name='', **params):
    '''
    Averages across trials in each condition and saves a plot

    Arguments:
            epoched: An Epoched object, like the one one outputed by epoch()
            conds_to_plot: A list of indices of conditions to plot or 'all'
                                            To plot all conditions
            plot_colors: list of colors in hex format. E.g. '#00FF00'
            plot_style: list of style specs like ['-', ':']
            plot_error: True or False
            sample_rate: Sample rate of the eye tracker (hz)
            back_time: Time to plot before event (ms)
            plot_title: Title of the plot
            plot_fname: File name of the saved image
            out_dir: Outputs will be saved to this directory
            base_name: string is appended to output files

    '''
    print('\nPlotting...\n')

    # Calulates the mean and errors (ignoring nans), supress warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        errors = stat.sem(epoched.matrix, axis=2, ddof=1, nan_policy='omit')
        flattened = np.nanmean(epoched.matrix, axis=2)

    if conds_to_plot == 'all':
        conds_to_plot = [i for i in range(epoched.n_categs)]
    assert len(plot_colors) >= len(
        conds_to_plot), 'Require more colors than plotted conditions'
    assert len(plot_style) > len(
        conds_to_plot), 'Require more styles than plotted conditions'
    x = [1000 * i / sample_rate -
         back_time for i in range(epoched.total_samples)]

    fig, ax = plt.subplots()
    fig.set_size_inches(8, 5)

    # i is the index of the condition, count is the order of plotting
    for count, i in enumerate(conds_to_plot):
        y = flattened[i, :]
        ax.plot(x, y, label=epoched.names[i], color=plot_colors[count],
                ls=plot_style[count])

        # Plot error bars
        if plot_error:
            err = errors[i, :]
            ax.fill_between(x, y - err, y + err,
                            alpha=0.25, color=plot_colors[count])

    # Formatting...
    plt.xlim((x[0], x[-1]))
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])
    ax.legend(bbox_to_anchor=(1, 1.04), frameon=False)
    plt.title(plot_title)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.savefig(make_path(plot_fname, '.png', out_dir=out_dir, base_name=base_name),
                bbox_inches='tight', dpi=600)


if __name__ == '__main__':
    params = params.get_params(sys.argv)
    fname = select_files('.pkl')[0]
    params['out_dir'] = os.path.dirname(fname)
    print(fname)
    e = load_pkl(fname)
    plot_conds(e, **params)
