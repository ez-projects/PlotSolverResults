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


mypath = os.path.dirname(os.path.realpath(__file__))
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

filename = ""
if len(sys.argv) < 2:
    sys.exit('ERROR: No file was give to plot!!!')
else:
    filenames = sys.argv[1:]

for filename in filenames:
    print "Start plotting: {}".format(filename)

    df = pd.read_csv(filename)
    df.head()

    # Get x-axis values based on number of intervals
    # num_intervals = 20
    # xinterval = find_interval(float(df.Timesteps.values[-1]), num_intervals)
    # print "xinterval: %f" % xinterval
    
    x = df.Mesh_Sizes
    # pdb.set_trace()
    # sys.exit()
    # timesteps = df.Timesteps
    # for i, value in enumerate(timesteps):
    #     if i % xinterval == 0:
    #         x.append(value)
    
    # Get y values from each solver based on x (timestep 1-base)
    # data = {}
    # for key, value in df.iteritems():
    #     if key != "Timesteps":
    #         data.update({key: []})
    #         for i in x:
    #             v = float(value.values[i-1]/60.0/60.0)
    #             data[key].append(v)
    #             if v >= maxy:
    #                 maxy = v
    
    # maxx = float(df.Timesteps.values[-1])
    # X-Axis is mesh sizes, i.e. from 0 to 1,200,000
    # xmajor_ticks = np.arange(0, 1200000, 100000)
    # xminor_ticks = np.arange(0, 1200000, 50000)

    
    # yinterval = round(float(maxy/num_intervals), 2)
    # Y-Axis is the total solve time in hours, i.e. from 0 to 100
    # ymajor_ticks = np.arange(0, 110, 10)
    # yminor_ticks = np.arange(0, 110, 5)
    
    fig, ax = plt.subplots()

    ax.set_xlim(0, 1200000)
    ax.set_ylim(0, 130)

    # Set y-tickets to be 2 decimal places
    # http://stackoverflow.com/questions/12608788/changing-the-tick-frequency-on-x-or-y-axis-in-matplotlib
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.2f'))
    label_font = 7
    ax.set_xlabel('Mesh Sizes', fontsize=label_font)
    ax.set_ylabel('Total Solve Time (h)', fontsize=label_font)
    labels = []
    for i in df.Mesh_Sizes:
        labels.append(i)
    ax.xaxis.set_ticks(df.Mesh_Sizes)
    ax.set_xticklabels(df.Mesh_Sizes)
    
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
    for key, value in df.iteritems():
        if key != 'Mesh_Sizes':
            plt.plot(x, df[key], styles[i]+'-', label=key, markersize=7.0, linewidth=2.0)
            i += 1
    
    plt.legend(prop={'size':label_font}, loc='upper left')

    # Following lines are used to drop major and minor tickes and lines
    # ax.grid(which='minor', alpha=0.2)                                                
    # ax.grid(which='major', alpha=0.8)
    # ax.set_xticks(xmajor_ticks)                                                       
    # ax.set_xticks(xminor_ticks, minor=True)
    # ax.set_yticks(ymajor_ticks)
    # ax.set_yticks(yminor_ticks, minor=True)

    # Save figures in both eps and png formats
    plt.savefig(filename.replace('.csv', '.eps'), format='eps')
    plt.savefig(filename.replace('.csv', '.png'), format='png')
    
    # Show figure to the screen
    plt.show()