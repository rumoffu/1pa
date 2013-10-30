#!/usr/bin/env python
"""
@author Deepak Lingam and Kyle Wong
This is a driver program to run a Point Cloud to Point Cloud Registration
and a Pivot Calibration.
"""
#import matplotlib.pyplot as plt  
import numpy as np 


def main():
	"""
	Program to open a data set
	and do a point cloud to point cloud registration
	"""

	#open data set
	ptcloud_d = []
	ptcloud_a = []
	ptcloud_c = []
	ptcloud_d, ptcloud_a, ptcloud_c = readCalbody("../input_data/pa1-debug-a-calbody.txt")
	ptcloud_frame = readCalreadings("../input_data/pa1-debug-a-calreadings.txt")

	##print " d: \n%s\n a: \n%s\n c: \n%s\n " % (ptcloud_d, ptcloud_a, ptcloud_c)
	##print " frame: \n%s\n" % ptcloud_frame
	
def readCalbody(txt):
	import numpy as np
	ptcloud_d = []
	ptcloud_a = []
	ptcloud_c = []
	
	calbody = open(txt, 'r')
	header = calbody.readline().split(',')
	N_D = int(header[0].strip())
	N_A = int(header[1].strip())
	N_C = int(header[2].strip())
	calbody_fn = header[3]

	for i in range(N_D):
		ptcloud_d.append(float(calbody.readline().split(',')[0].strip()))
	for i in range(N_A):
		ptcloud_a.append(float(calbody.readline().split(',')[1].strip()))
	for i in range(N_C):
		ptcloud_c.append(float(calbody.readline().split(',')[2].strip()))
	return ptcloud_d, ptcloud_a, ptcloud_c

def readCalreadings(txt):
	import numpy as np
	ptcloud_d = []
	ptcloud_a = []
	ptcloud_c = []
	ptcloud_frame = []

	calreadings = open(txt, 'r')
	header = calreadings.readline().split(',')
	N_D = int(header[0])
	N_A = int(header[1])
	N_C = int(header[2])
	N_frames = int(header[3])
	calreadings_fn = header[4]


	for j in range(N_frames):
		for i in range(N_D):
			ptcloud_d.append(float(calreadings.readline().split(',')[0].strip()))
		for i in range(N_A):
			ptcloud_a.append(float(calreadings.readline().split(',')[1].strip()))
		for i in range(N_C):
			ptcloud_c.append(float(calreadings.readline().split(',')[2].strip()))
		ptcloud_frame.append([ptcloud_d, ptcloud_a, ptcloud_c])

	return ptcloud_frame

'''
	fdata = np.genfromtxt('sortedfred.csv', delimiter=',', skip_header=1,
	                     skip_footer=0, names=['id', 'min'])
	
	ddata = np.genfromtxt('sorteddock.csv', delimiter=',', skip_header=1,
	                     skip_footer=0, names=['id', 'min'])
	
	ax1.scatter(fdata['min'],ddata['min'],label='dock6', color='blue')
'''
	
if __name__ == '__main__':
    main()
