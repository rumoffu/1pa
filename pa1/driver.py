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

	for i in range(len(ptcloud_frame)):
		print ptcloud_frame[i]
	#for cloudframe in ptcloud_frame:
'''		frame_d = findFrame(ptcloud_d, cloudframe)
		frame_a = 
			Frame F_C = (F_D.inverse()).dot(F_A);
			PointCloud C = F_C.dot(c);
			Cs[i] = C;
'''	
def findFrame(bodycloud, readingscloud):
	return 0

def readCalbody(txt):
	import numpy as np

	calbody = open(txt, 'r')
	header = calbody.readline().split(',')
	N_D = int(header[0].strip())
	N_A = int(header[1].strip())
	N_C = int(header[2].strip())
	calbody_fn = header[3]

	ptcloud_d = readCloud(calbody, N_D)
	ptcloud_a = readCloud(calbody, N_A)
	ptcloud_c = readCloud(calbody, N_C)
	return ptcloud_d, ptcloud_a, ptcloud_c

def readCloud(openfile, num):
	cloud = []
	for i in range(num):
		row = []
		for xyz in openfile.readline().split(','):
			row.append(float(xyz.strip()))
		cloud.append(row)
	return cloud

def readCalreadings(txt):
	import numpy as np
	ptcloud_frame = []

	calreadings = open(txt, 'r')
	header = calreadings.readline().split(',')
	N_D = int(header[0])
	N_A = int(header[1])
	N_C = int(header[2])
	N_frames = int(header[3])
	calreadings_fn = header[4]

	for j in range(N_frames):
		ptcloud_d = readCloud(calreadings, N_D)
		ptcloud_a = readCloud(calreadings, N_A)
		ptcloud_c = readCloud(calreadings, N_C)
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
