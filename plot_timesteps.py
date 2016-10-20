#!/usr/bin/python
import numpy as np
import pandas as pd
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import matplotlib.pyplot as plt

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
    print 'Start plotting: {}'.format(filename)

    df = pd.read_csv(filename)
    df.head()

    # X axis
    # timestep = df.Timesteps
    # x = timestep
    # AMG_Class_time = df['AMG Class']

    fig, ax = plt.subplots()

    # fig = plt.figure()                                                               
    # ax = fig.add_subplot(1,1,1) 
    # major ticks every 20, minor ticks every 5                                      
    major_ticks = np.arange(0, int(timestep[-1])+1, 100)                                              
    # minor_ticks = np.arange(0, 101, 5)                                               

    ax.set_xticks(major_ticks)                                                       
    # ax.set_xticks(minor_ticks, minor=True)                                           
    ax.set_yticks(major_ticks)                                                       
    # ax.set_yticks(minor_ticks, minor=True)                                           

    # and a corresponding grid                                                       

    # ax.grid(which='both')                                                            

    # or if you want differnet settings for the grids:                               
    # ax.grid(which='minor', alpha=0.2)                                                
    # ax.grid(which='major', alpha=0.5)



    plt.xlabel('Timesteps')

    # plt.xlim(0, 10)
    plt.ylabel('Time (h)')
    # plt.ylim(0, 1000)


    title = filename.replace('.csv', '').replace('_', ' ').title()
    plt.title(title)
    # plt.xticks(x, labels, rotation='vertical')
    # styles = ['o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd']
    styles = ['^', 'o', 'd', 's', 'p', '+', '.', 'D', 'x', '|', '*']
    i = 0
    # pdb.set_trace()
    for key, value in df.iteritems():
        if key != 'Timesteps':
            plt.plot(x.values, value.values, styles[i]+'-', label=key)
            i += 1

    # ax.set_xticks(x)
    # ax.grid(b=True, which='major')
    # ax.grid(b=True, which='minor')                                                      
    plt.legend(prop={'size':12}, loc='upper left')
    plt.grid()

    plt.savefig(filename.replace('.csv', '.eps'), format='eps')
    plt.savefig(filename.replace('.csv', '.png'), format='png')
    plt.show()