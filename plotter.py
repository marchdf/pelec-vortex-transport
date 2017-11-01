#!/usr/bin/env python3

# ========================================================================
#
# Imports
#
# ========================================================================
import argparse
import sys
import os
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd


# ========================================================================
#
# Some defaults variables
#
# ========================================================================
plt.rc('text', usetex=True)
plt.rc('font', family='serif', serif='Times')
cmap_med = ['#F15A60', '#7AC36A', '#5A9BD4', '#FAA75B',
            '#9E67AB', '#CE7058', '#D77FB4', '#737373']
cmap = ['#EE2E2F', '#008C48', '#185AA9', '#F47D23',
        '#662C91', '#A21D21', '#B43894', '#010202']
dashseq = [(None, None), [10, 5], [10, 4, 3, 4], [
    3, 3], [10, 4, 3, 4, 3, 4], [3, 3], [3, 3]]
markertype = ['s', 'd', 'o', 'p', 'h']


# ===============================================================================
#
# Function definitions
#
# ===============================================================================
def parse_ic(fname):
    """
    Parse the file written by PeleC to understand the initial condition

    Returns a dictionary for easy acces
    """

    # Read into dataframe
    df = pd.read_csv(fname)
    df.rename(columns=lambda x: x.strip(), inplace=True)

    # convert to dictionary for easier access
    return df.to_dict('records')[0]


# ========================================================================
#
# Main
#
# ========================================================================
if __name__ == '__main__':

    # ========================================================================
    # Parse arguments
    parser = argparse.ArgumentParser(
        description='A simple plot tool')
    parser.add_argument(
        '-s', '--show', help='Show the plots', action='store_true')
    args = parser.parse_args()

    resolutions = ['32', '64', '128', '256', '512', '1024']
    time_nd = 1
    L = 10
    Omega = L**2
    icname = 'ic.txt'
    fname = 'error2.curve'

    # Now loop on post-processing directories
    lst = []
    for k, res in enumerate(resolutions):

        # get problem definition from output file
        ics = parse_ic(os.path.join(res, icname))
        print(ics)

        df = pd.read_csv(os.path.join(res, fname),
                         header=0,
                         names=['time', 'error2'],
                         delim_whitespace=True)

        df['error'] = np.sqrt(df['error2'] / Omega)
        df['resolution'] = float(res)
        lst.append(df)

        # Plot a time history of the error
        plt.figure(0)
        p = plt.semilogy(df['time'][0::2] / ics['tau'],
                         df['error'][0::2],
                         ls='-',
                         lw=2,
                         color=cmap[k],
                         label=res)

    df = pd.concat(lst)

    # Just plot the last time
    subdf = df.loc[2 * time_nd]
    plt.figure(1)
    plt.title('At t = {0:d}'.format(time_nd))
    p = plt.loglog(subdf['resolution'],
                   subdf['error'],
                   ls='-',
                   lw=2,
                   color=cmap[0],
                   marker=markertype[0],
                   mec=cmap[0],
                   mfc=cmap[0],
                   ms=10,
                   label='Pele')

    # Theoretical error
    theory_order = 2.0
    theory = subdf['error'].iloc[-1] * \
        (subdf['resolution'].iloc[-1] / subdf['resolution'])**theory_order

    p = plt.loglog(subdf['resolution'],
                   theory,
                   ls='-',
                   lw=2,
                   color=cmap[-1],
                   label='2nd order')

    plt.figure(0)
    ax = plt.gca()
    plt.xlabel(r"$t~[-]$")
    plt.ylabel(r"Error")
    legend = ax.legend(loc='best')
    plt.savefig('time_history.png', format='png')

    plt.figure(1)
    ax = plt.gca()
    plt.xlabel(r"$N$")
    plt.ylabel(r"Error")
    legend = ax.legend(loc='best')
    plt.savefig('error_{0:d}.png'.format(time_nd), format='png')
