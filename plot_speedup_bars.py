#!/usr/bin/python
import numpy as np
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import sys
from os import listdir
import os
from os.path import isfile, join

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
    if not 'speedup' in filename:
        sys.exit('ERROR: File name error, this script only print speedup results.')

    print 'Start plotting: {}'.format(filename)

    with open(filename) as f:
      raw_data = f.read()
    raw_data = raw_data.split('\n')

    print 'Raw Data: \n{}'.format(raw_data)

    plot_data = []
    for row in raw_data:
        if row and not row[0].startswith('#'):
          plot_data.append(row)

    print 'Data: \n{}'.format(plot_data)
    plt_data = {}
    for d in plot_data:
        key = d.split(' ')[0]
        values = []
        if key != 'Matrix':
          for v in d.split(' ')[1:]:
            values.append(float(v))
        else:
          for v in d.split(' ')[1:]:
            values.append(v)
        plt_data.update(
          {
            key: values
          }
        )

    # import collections
    # plt_data = collections.OrderedDict(sorted(plt_data.items()))

    print len(plt_data)
    fig, ax = plt.subplots()
    n_groups = len(plt_data['Matrix'])
    print 'n_groups = {}'.format(n_groups)
    index = np.arange(n_groups)
    print 'index = {}'.format(index)
    bar_width = 0.2

    # opacity = 0.4
    # error_config = {'ecolor': '0.3'}

    print plt_data
    # sys.exit()

    colors = ['r', 'b', 'c', 'y', 'g']
    offset = 0
    for key in plt_data.keys():
    	if key != 'Matrix':
    		value = plt_data[key]
    		print value
    		result = plt.bar(index+bar_width*offset, value, bar_width,
                     # alpha=opacity,
                     color=colors[offset],
                     # yerr=std_men,
                     # error_kw=error_config,
                     label=key.replace('-', ' '))
    		offset += 1

    # value = (0.93, 0.58, 0.88)
    # rects1 = plt.bar(index+bar_width*0, value, bar_width,
    #                  # alpha=opacity,
    #                  color='b',
    #                  # yerr=std_men,
    #                  # error_kw=error_config,
    #                  label='GmresDiag_d')
    # value = (4.64, 2.91, 4.64)
    # rects2 = plt.bar(index+bar_width*1.0, value, bar_width,
    #                  # alpha=opacity,
    #                  color='r',
    #                  # yerr=std_men,
    #                  # error_kw=error_config,
    #                  label='CgDiag_d')

    # value = (5.00, 2.00, 4.00)
    # rects2 = plt.bar(index+bar_width*2.0, value, bar_width,
    #                  # alpha=opacity,
    #                  color='y',
    #                  # yerr=std_men,
    #                  # error_kw=error_config,
    #                  label='Test_d')

    # set y-axis range
    plt.ylim(0, 35)
    ax.grid(b=True, which='major')
    ax.grid(b=True, which='minor')                                                      
    plt.legend(prop={'size':12}, loc='upper left')
    plt.xlabel('Number of Nodes')
    plt.ylabel('Speedup')
    # plt.title(filename.replace('_', ' ').replace('results.dat', '').title())
    plt.xticks(index + bar_width, plt_data['Matrix'])
    ax.grid(b=True, which='major')
    ax.grid(b=True, which='minor')


    plt.tight_layout()
    plt.savefig(filename.replace('.dat', '.eps'), format='eps')
    plt.savefig(filename.replace('.dat', '.png'), format='png')
    plt.show()
