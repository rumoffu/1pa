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
	import sys

	#Problem 4
	#open data set
	ptcloud_d, ptcloud_a, ptcloud_c = readCalbody("../input_data/pa1-debug-a-calbody.txt")
	ptcloud_frame = readCalreadings("../input_data/pa1-debug-a-calreadings.txt")

	##print " d: \n%s\n a: \n%s\n c: \n%s\n " % (ptcloud_d, ptcloud_a, ptcloud_c)
	##print " frame: \n%s\n" % ptcloud_frame
	frameAns = []
	c_expected = []
	for i in range(len(ptcloud_frame)):
		#Problem 4a
		#print ptcloud_frame[0, i]
		frame_d = solveFrame(ptcloud_d, ptcloud_frame[i, 0]) #frame is ptclouds d, a, c
		#Problem 4b
		frame_a = solveFrame(ptcloud_a, ptcloud_frame[i, 1]) #frame is ptclouds d, a, c
		#Problem 4c
		###frame_c = frame_d.inverse().dot(frame_a)

		###ci_expected = frame_c.rotation*ptcloud_c.T + frame_c.displacement
		ci_a = frame_a.rotation*ptcloud_c.T + frame_a.displacement
		frame_di = frame_d.inverse()
		ci_expected = frame_di.rotation*ci_a + frame_di.displacement
		c_expected.append(ci_expected)
		frameAns.append(ptcloud_frame[i, 2])
	#print c_expected
	nice_c_expected = getFormat(c_expected)
	diff = nice_c_expected - np.vstack(frameAns)
	##printOutput(c_expected)
	##print nice_c_expected
	##print diff

	#Problem 5
	

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

def printOutput(c_expected):
	import sys
	# 8 c expected's
	for c in c_expected:
		##print c.shape
		numrow, numcol = c.shape
		# 27 frames for each c
		for row in range(numcol):
			# 3 times
			for col in range(numrow):
				sys.stdout.write(str(c[col, row]) + ',\t')
			sys.stdout.write('\n')
	

def getFormat(c_expected):
	import numpy as np
	from numpy import matrix

	bigset = []
	# 8 c expected's
	for c in c_expected:
		##print c.shape
		numrow, numcol = c.shape
		# 27 frames for each c
		acloud = []
		for row in range(numcol):
			# 3 times
			arow = []
			for col in range(numrow):
				arow.append(c[col, row])
			#aset.append(arow)
			acloud.append(arow)
		bigset.append(acloud)
	
	final = np.vstack(bigset)
	return final

def solveFrame(a, b):
	from numpy import linalg as LA
	abar = getMidpoint(a)
	bbar = getMidpoint(b)
	anorm = a - abar
	bnorm = b - bbar

	matrixH = H(anorm, bnorm)	
	matrixG = G(matrixH)
	eigvals, eigvects = LA.eig(matrixG)
	for i in range(len(eigvals)):
		maxval = max(eigvals)
		if eigvals[i] == maxval:
			maxi = i
	maxvect = eigvects[maxi]	
	
	R = getR(maxvect)
	##print abar
	##print bbar
	displace = bbar.T - R*abar.T
	##print displace
	return Frame(R, displace)

def findDisplacement(clouda, cloudb):
	return getMidpoint(cloudb) - getMidpoint(clouda)
	
def getMidpoint(cloud):
	import numpy as np
	from numpy import matrix
	
	xyz = []
	xsum = 0
	ysum = 0
	zsum = 0
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
	##print H
	return H

def G(h):
	import numpy as np
	from numpy import matrix
	identity = np.identity(3)
	trace = np.trace(h)
	delta = matrix([ h[1,2]-h[2,1], h[2,0] - h[0,2], h[0,1]-h[1,0] ]).T
	bot = h + h.T - trace*identity
	row1 = np.hstack([matrix(trace), delta.T])
	botrows = np.hstack([delta, bot])
	G = np.vstack([row1, botrows])
	##print G
	return G
	
def getR(maxeigvect):
	import numpy as np
	from numpy import matrix
	q0 = maxeigvect[0, 0]
	q1 = maxeigvect[0, 1]
	q2 = maxeigvect[0, 2]
	q3 = maxeigvect[0, 3]

	row1 = np.hstack([ [q0*q0 + q1*q1 - q2*q2 - q3*q3],	[2*(q1*q2 - q0*q3)], 		[2*(q1*q3 + q0*q2)] 		])
	row2 = np.hstack([ [2*(q1*q2 + q0*q3) ],		[q0*q0 - q1*q1 + q2*q2 - q3*q3],[2*(q2*q3 - q0*q1)] 		])
	row3 = np.hstack([ [2*(q1*q3 - q0*q2) ],		[2*(q2*q3 + q0*q1)],		[q0*q0 - q1*q1 - q2*q2 + q3*q3] ])
	R = np.vstack([row1, row2, row3])
	##print R
	return matrix(R)


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

if __name__ == '__main__':
    main()
