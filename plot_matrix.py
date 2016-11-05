#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import os, sys, pdb
from matplotlib import colors

size = 0
filename = ''
if len(sys.argv) == 2:
	matrix = sys.argv[1].replace('ElemMatrix', '')
	size = int(matrix)
	filename = 'ElemMatrix' + matrix
	print 'Start plotting: {}\n...\n...'.format(filename)
else:
	sys.exit('Need matrix size as input!!!')

# print os.listdir('/home/nathan/CUDAprojects/ElemMatrVect')

filepath = '/home/nathan/CUDAprojects/ElemMatrVect'
if 'ElemMatrix' in sys.argv[1]:
	filepath = '.'
xvalues = []		# column index
yvalues = []		# row index
if filename in os.listdir(filepath):
	with open(filepath + '/' + filename) as f:
		data = f.read()
		data = data.split('\n')
		start_pos = 5
		aa = np.zeros((size, size))
		for i in xrange(start_pos, len(data)):
			# print data[i].split('\t')
			if data[i]:
				x = int(data[i].split('\t')[0])
				# print 'x = {}'.format(x)
				y = size - int(data[i].split('\t')[1]) - 1
				# print 'y = {}'.format(y)
				v = float(data[i].split('\t')[2])

				xvalues.append(x)
				yvalues.append(y)
fig, ax = plt.subplots()
plt.xlim(0, size-1)
plt.ylim(0, size-1)
ax.set_xticks([]) 
ax.set_yticks([])
plt.scatter(xvalues, yvalues, c='0.1', marker='.', s=1.0)
plt.savefig(filename + '.eps', format='eps')
plt.savefig(filename + '.png', format='png')
plt.show()