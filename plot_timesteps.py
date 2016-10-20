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

def get_max_time(df):
    max_time = float(0.0)
    for key, solvers in df.iteritems():
        if key != "Timesteps":
            solver_time = float(solvers.values[-1])
            
            if solver_time > max_time:
                print "swap"
                max_time = solver_time
            print "solver_time: %.2f " % solver_time
            print "max_time: %.2f " % max_time
    return max_time



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
    x = []
    timesteps = df.Timesteps
    for i, value in enumerate(timesteps):
        if i % 200 == 0:
            x.append(value)
    # pdb.set_trace()
    data = {}
    for key, value in df.iteritems():
        if key != "Timesteps":
            data.update({key: []})
            for i, v in enumerate(value.values):
                if i % 200 == 0:
                    data[key].append(float(v))

    fig, ax = plt.subplots()

    # fig = plt.figure()                                                               
    # ax = fig.add_subplot(1,1,1) 
    # major ticks every 20, minor ticks every 5                                      
    # major_ticks = np.arange(0, int(timestep[-1])+1, 100)                                              
    maxx = float(x[-1])
    print "maxx: %.2f " % maxx
    xmajor_ticks = np.arange(0, maxx+200, 200)                                                       
    xminor_ticks = np.arange(0, maxx+200, 100)
    
    maxy = get_max_time(df)
    print "maxy: %.2f " % maxy
    ymajor_ticks = np.arange(0, maxy+200, 200)
    yminor_ticks = np.arange(0, maxy+200, 100)                                               

    ax.set_xticks(xmajor_ticks)                                                       
    ax.set_xticks(xminor_ticks, minor=True)                                           
    ax.set_yticks(ymajor_ticks)                                                       
    ax.set_yticks(yminor_ticks, minor=True)                                           

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

    # ax.set_xticks(x)
    ax.grid(b=True, which='major')
    ax.grid(b=True, which='minor')                                                      
    
    # plt.grid()
    # plt.xticks(x, labels, rotation='vertical')
    # styles = ['o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd']
    styles = ['^', 'o', 'd', 's', 'p', '+', '.', 'D', 'x', '|', '*']
    i = 0
    # Now add the legend with some customizations.
    legend = ax.legend(loc='upper left', shadow=True)
    count = 0
    for key, value in data.iteritems():
        if key != 'Timesteps':
            plt.plot(x, data[key], styles[i]+'-', label=key)
            i += 1
    plt.legend(prop={'size':12}, loc='upper left')
    plt.savefig(filename.replace('.csv', '.eps'), format='eps')
    plt.savefig(filename.replace('.csv', '.png'), format='png')
    plt.show()