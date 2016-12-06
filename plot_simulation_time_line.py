#!/usr/bin/python
import numpy as np
import pandas as pd
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import sys
from os import listdir
import os
from bson.json_util import dumps
from os.path import isfile, join
import pdb

from cycler import cycler

from constants import STYLES as styles
from constants import SOLVERS as solvers

def convert_duration_to_time(duraton):
    d = duraton.split(':')
    if len(d) == 4:
        s = 0.0
        for i in xrange(len(d)):
            p = len(d)-i-2
            if p > 0:
                s += int(d[i]) * pow(60, p)
            else:
                s += int(d[i]) / 1000.0
        # print s
        return s
    else:
        sys.exit('Invalid duration format entered, only accept: 00:00:00:000')

def get_max_time(df):
    max_time = float(0.0)
    for key, solvers in df.iteritems():
        if key != "Timesteps":
            solver_time = float(solvers.values[-1])
            
            if solver_time > max_time:
                # print "swap"
                max_time = solver_time
            # print "solver_time: %.2f " % solver_time
            # print "max_time: %.2f " % max_time
    return max_time

def find_interval(total_timesteps, num_intervals):
    """
    calcuate the interval base from number of intervals and total number of timesteps
    """
    for i in xrange(20, 1000, 20):
        if total_timesteps / i <= num_intervals:
            return i

mypath = os.path.dirname(os.path.realpath(__file__))
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

filename = ''
if len(sys.argv) < 2:
    sys.exit('ERROR: No file was give to plot!!!')
else:
    filenames = sys.argv[1:]

for filename in filenames:
    print 'Start plotting: {}'.format(filename)

    df = pd.read_csv(filename)
    df.head()

    # Get x-axis values based on number of intervals
    num_intervals = 10
    xinterval = 0.05
    # xinterval = find_interval(float(df.Simulated_Time.values[-1]), num_intervals)
    print "xinterval: %f" % xinterval
    
    x = []
    simulated_time = df.Simulated_Time
    x = simulated_time
    # for i, value in enumerate(simulated_time):
    #     if i % xinterval == 0:
    #         x.append(value)
    
    # Get y values from each solver based on x (timestep 1-base)
    data = {}
    maxy = 0.0
    for key, value in df.iteritems():
        # pdb.set_trace()
        if key != "Simulated_Time":
            data.update({key: []})
            for v in value.values:
                v_h = float(v/3600.0)
                data[key].append(v_h)
                if v_h >= maxy:
                    maxy = v_h
    maxx = 0.5
    xmajor_ticks = np.arange(0, maxx+xinterval, xinterval)
    xminor_ticks = np.arange(0, maxx+xinterval, 0.01)
    
    fig, ax = plt.subplots()
    yinterval = round(float(maxy/num_intervals), 2)
    if yinterval < 1.0:
        yinterval = round(yinterval, 1)
    else:
        yinterval = int(yinterval)

    ymajor_ticks = np.arange(0, maxy+yinterval, yinterval)
    yminor_ticks = np.arange(0, maxy+yinterval, yinterval*0.5)
    # Set y-tickets to be 2 decimal places
    # http://stackoverflow.com/questions/12608788/changing-the-tick-frequency-on-x-or-y-axis-in-matplotlib
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.2f'))

    label_font = 10
    ax.set_xlabel('Simulation Time (sec)', fontsize=label_font)
    ax.set_ylabel('CPU Time (h)', fontsize=label_font)
    # Set x and y tick labels' font
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(label_font)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(label_font)

    # Add title to chart
    # title = filename.replace('.csv', '').replace('_', ' ').title()
    # plt.title(title)                                                   
    
    # colors = ['r', 'b', 'c', 'y', 'g', 'm', 'k']
    i = 0
    # Now add the legend with some customizations.
    # Line properties: http://matplotlib.org/users/pyplot_tutorial.html
    ax.set_prop_cycle(cycler('color', ['r', 'b', 'c', 'y', 'g', 'm', 'k']) )
    for solver in solvers:
        if solver != 'Simulated_Time':
            plt.plot(x, data[solver], styles[i]+'-', label=solver, linewidth=2.0, markersize=8.0)
            i += 1
    
    # Order the lengeds 
    handles,labels = ax.get_legend_handles_labels()
    # handles.sort()
    # labels.sort()
    legend = ax.legend(handles, labels, loc='upper left', shadow=True, fontsize=label_font)

    # Following lines are used to drop major and minor tickes and lines
    ax.grid(which='minor', alpha=0.2)                                                
    ax.grid(which='major', alpha=0.8)
    ax.set_xticks(xmajor_ticks)                                                       
    ax.set_xticks(xminor_ticks, minor=True)
    ax.set_yticks(ymajor_ticks)
    ax.set_yticks(yminor_ticks, minor=True)

    # Save figures in both eps and png formats
    path = './plots/'
    plt.savefig(path + filename.replace('.csv', '.eps').replace('raw_data/', '').replace('_new', ''), format='eps')
    plt.savefig(path + filename.replace('.csv', '.png').replace('raw_data/', '').replace('_new', ''), format='png')
    
    # Show figure to the screen
    plt.show()