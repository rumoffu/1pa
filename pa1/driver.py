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
	#ptcloud_d = []
	#ptcloud_a = []
	#ptcloud_c = []
	ptcloud_d, ptcloud_a, ptcloud_c = readCalbody("../input_data/pa1-debug-a-calbody.txt")
	ptcloud_frame = readCalreadings("../input_data/pa1-debug-a-calreadings.txt")

	##print " d: \n%s\n a: \n%s\n c: \n%s\n " % (ptcloud_d, ptcloud_a, ptcloud_c)
	##print " frame: \n%s\n" % ptcloud_frame

	for i in range(len(ptcloud_frame)):
		frame_d = solveFrame(ptcloud_d, ptcloud_frame[i, 0]) #frame is ptclouds d, a, c
		frame_a = solveFrame(ptcloud_a, ptcloud_frame[i, 1]) #frame is ptclouds d, a, c
		frame_c = frame_d.inverse.dot(frame_a)
		c_expected.append(frame_c.rotation*ptcloud_c + frame_c.displacement)
'''		frame_d = solveFrame(ptcloud_d, cloudframe)
		frame_a = 
			Frame F_C = (F_D.inverse()).dot(F_A);
			PointCloud C = F_C.dot(c);
			Cs[i] = C;
'''	
class Frame:
	def __init__(self, rotation, displacement):
		self.rotation = rotation #matrix
		self.displacement = displacement #matrix

	def dot(self, otherFrame):
		rot = self.rotation*otherFrame.rotation
		displace = self.rotation*otherFrame.displacement + self.displacement
		return Frame(rot, displace)
	
	def inverse(self):
		rot = self.rotation.I #matrix inverse
		displace = -1*rot*self.displacement
		return Frame(rot, displace)


def solveFrame(a, b):
	#displacement = findDisplacement(a, b)
	anorm = a - getMidpoint(a)
	bnorm = b - getMidpoint(b)

	matrixH = H(anorm, bnorm)	
	matrixG = G(matrixH)
	return Frame(rot, displace)

def findDisplacement(clouda, cloudb):
	return getMidpoint(cloudb) - getMidpoint(clouda)
	
def getMidpoint(cloud):
	import numpy as np
	from numpy import matrix
	
	xyz = []
	xsum = 0
	ysum = 0
	zsum = 0
	#print cloud[0,0]
	for i in range(len(cloud)):
		xsum += cloud[i, 0]
		ysum += cloud[i, 1]
		zsum += cloud[i, 2]
	
	size = len(cloud)
	xyz.append([xsum/size, ysum/size, zsum/size])
	return matrix(xyz)

def H(a, b):
	import numpy as np
	from numpy import matrix

	H = np.zeros(shape=(3,3))
	for i in range(len(a)):
		summand = np.zeros(shape=(3,3))
		ai = a[i]
		bi = b[i]
		for j in range(3):
			for k in range(3):
				summand[j, k] = ai[0, j] * bi[0, k]
		H = H + summand
	print H
	return H

def G(h):
	import numpy as np
	from numpy import matrix
	identity = np.identity(3)
	trace = np.trace(h)
	delta = matrix([ h[1,2]-h[2,1], h[2,0] - h[0,2], h[0,1]-h[1,0] ])
	bot = h + h.T - trace*identity

	row1 = np.hstack([matrix(trace), delta])
	print row1
	botrows = np.hstack([delta.T, bot])
	print botrows
	G = np.vstack([row1, botrows])
	print G
	return G
	

def readCalbody(txt):
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
	import numpy as np
	from numpy import matrix
	cloud = []
	for i in range(num):
		row = []
		for xyz in openfile.readline().split(','):
			row.append(float(xyz.strip()))
		cloud.append(row)
	#print"cloud \n%s" % cloud
	#print "matrix \n %s" % matrix(cloud)
	return matrix(cloud)

def readCalreadings(txt):
	import numpy as np
	from numpy import matrix	
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

	return matrix(ptcloud_frame)

	'''
		fdata = np.genfromtxt('sortedfred.csv', delimiter=',', skip_header=1,
		                     skip_footer=0, names=['id', 'min'])
		
		ddata = np.genfromtxt('sorteddock.csv', delimiter=',', skip_header=1,
		                     skip_footer=0, names=['id', 'min'])
		
		ax1.scatter(fdata['min'],ddata['min'],label='dock6', color='blue')
	'''
		
if __name__ == '__main__':
    main()
