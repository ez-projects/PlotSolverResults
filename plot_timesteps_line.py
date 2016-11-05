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
    xinterval = find_interval(float(df.Timesteps.values[-1]), num_intervals)
    print "xinterval: %f" % xinterval
    
    x = []
    timesteps = df.Timesteps
    for i, value in enumerate(timesteps):
        if i % xinterval == 0:
            x.append(value)
    
    # Get y values from each solver based on x (timestep 1-base)
    data = {}
    maxy = 0.0
    for key, value in df.iteritems():
        if key != "Timesteps":
            data.update({key: []})
            for i in x:
                v = float(value.values[i-1]/60.0/60.0)
                data[key].append(v)
                if v >= maxy:
                    maxy = v
    
    maxx = float(df.Timesteps.values[-1])
    xmajor_ticks = np.arange(0, maxx+xinterval, xinterval)
    xminor_ticks = np.arange(0, maxx+xinterval, int(xinterval*0.5))
    
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
    ax.set_xlabel('Timesteps', fontsize=label_font)
    ax.set_ylabel('Time (h)', fontsize=label_font)
    # Set x and y tick labels' font
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(label_font)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(label_font)

    # Add title to chart
    # title = filename.replace('.csv', '').replace('_', ' ').title()
    # plt.title(title)                                                   
    
    # styles = ['o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd']
    styles = ['^', 'o', 'd', 's', 'p', '+', '.', 'D', 'x', '|', '*']
    i = 0
    # Now add the legend with some customizations.
    # Line properties: http://matplotlib.org/users/pyplot_tutorial.html
    legend = ax.legend(loc='upper left', shadow=True)
    for key, value in data.iteritems():
        if key != 'Timesteps':
            plt.plot(x, data[key], styles[i]+'-', label=key, markersize=6.0, linewidth=2.0)
            i += 1
    
    plt.legend(prop={'size':label_font}, loc='upper left')

    # Following lines are used to drop major and minor tickes and lines
    ax.grid(which='minor', alpha=0.2)                                                
    ax.grid(which='major', alpha=0.8)
    ax.set_xticks(xmajor_ticks)                                                       
    ax.set_xticks(xminor_ticks, minor=True)
    ax.set_yticks(ymajor_ticks)
    ax.set_yticks(yminor_ticks, minor=True)

    # Save figures in both eps and png formats
    plt.savefig(filename.replace('.csv', '.eps'), format='eps')
    plt.savefig(filename.replace('.csv', '.png'), format='png')
    
    # Show figure to the screen
    plt.show()