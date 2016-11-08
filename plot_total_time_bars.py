#!/usr/bin/python
import numpy as np
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import pandas as pd
import sys
from os import listdir
import os
from os.path import isfile, join
import pdb

mypath = os.path.dirname(os.path.realpath(__file__))
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# results_files = []
# for item in files:
#   if item.endswith('results.dat') and 'speedup' in item:
#     results_files.append(item)
# if not results_files:
#   sys.exit('No result data file found!!!')
filename = ''
if len(sys.argv) < 2:
    sys.exit('ERROR: No file was give to plot!!!')
else:
    filenames = sys.argv[1:]

for filename in filenames:
    # Check file name
    # if not filename.endswith('results.dat'):
    #     sys.exit('ERROR: File name format error, need end with "result.dat".')
    print 'Start plotting: {}'.format(filename)

    df = pd.read_csv(filename)
    df.head()

    print 'Raw Data: \n{}'.format(df)

    plot_data = []
    for row in df:
        if row and not row[0].startswith('#'):
          plot_data.append(row)
    print 'Data: \n{}'.format(plot_data)

    fig, ax = plt.subplots()
    # This is the number of rows in one column
    n_groups = len(plot_data) -3
    print 'n_groups = {}'.format(n_groups)
    index = np.arange(n_groups)
    print 'index = {}'.format(index)
    bar_width = 0.10

    ymax = 85
    if 'total_analysis' in filename:
        ymax = 130
    ymajor_ticks = np.arange(0, ymax, 10)
    yminor_ticks = np.arange(0, ymax, 5.0)

    print plot_data
    # sys.exit()

    colors = ['r', 'b', 'c', 'y', 'g', 'm', 'k', 'w']
    offset = 0
    for key, value in df.iteritems():
    	if key != 'Mesh_Sizes':
            print "offset = {}".format(offset)
            value = value.values
            print value
            result = plt.bar(index+bar_width*offset, value, bar_width,
                     # alpha=opacity,
                     color=colors[offset],
                     # yerr=std_men,
                     # error_kw=error_config,
                     label=key)
            offset += 1

    # set y-axis range
    plt.ylim(0, ymax)
    # Order the lengeds 
    handles,labels = ax.get_legend_handles_labels()
    handles.sort()
    labels.sort()
    legend = ax.legend(handles, labels, loc='upper left', shadow=True, fontsize=12)

    # plt.legend(prop={'size':12}, loc='upper left')
    plt.xlabel('Mesh Sizes')
    ylabel = filename.replace('raw_data/', '').replace('_', ' ').replace('.csv', '').title()
    ax.set_ylabel('{} (h)'.format(ylabel), fontsize=10)
    # plt.title(filename.replace('_', ' ').replace('results.dat', '').title())
    plt.xticks(index + bar_width, df.Mesh_Sizes)
    ax.set_yticks(ymajor_ticks)
    ax.set_yticks(yminor_ticks, minor=True)


    plt.tight_layout()
    path = './plots/'
    plt.savefig(path + filename.replace('.csv', '.eps').replace('raw_data/', ''), format='eps')
    plt.savefig(path + filename.replace('.csv', '.png').replace('raw_data/', ''), format='png')
    plt.show()
