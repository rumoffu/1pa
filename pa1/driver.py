#!/usr/bin/env python
"""
@author Deepak Lingam and Kyle Wong
This is a driver program to run a Point Cloud to Point Cloud Registration
and a Pivot Calibration.
"""

def main():
	"""
	Program to open a data set
	and do a point cloud to point cloud registration
	"""
	import sys
	prefix = "pa1-unknown-i"
	calbody_fn = "../input_data/" + prefix + "-calbody.txt"
	calreadings_fn = "../input_data/" + prefix + "-calreadings.txt"
	empivot_fn = "../input_data/" + prefix + "-empivot.txt"
	optpivot_fn = "../input_data/" + prefix + "-optpivot.txt"
	output_fn = "output/" + prefix + "-output.txt"
	aux_fn = "output/" + prefix + "-auxiliary.txt"

	#Problem 4
	#open data set
	ptcloud_d, ptcloud_a, ptcloud_c = readCalbody(calbody_fn)
	N_C = len(ptcloud_c)
	ptcloud_frame = readCalreadings(calreadings_fn)
	N_frames = len(ptcloud_frame)
	##print " d: \n%s\n a: \n%s\n c: \n%s\n " % (ptcloud_d, ptcloud_a, ptcloud_c)
	##print " cloudframe: \n%s\n" % ptcloud_frame
	frameAns = []
	c_expected = []
	#print len(ptcloud_frame) #8 times
	for i in range(len(ptcloud_frame)):
		#Problem 4a
		#print ptcloud_frame[0, i]
		frame_d = solveFrame(ptcloud_d, ptcloud_frame[i, 0]) #frame is ptclouds d, a, c

		#Problem 4b
		frame_a = solveFrame(ptcloud_a, ptcloud_frame[i, 1]) #frame is ptclouds d, a, c

		#Problem 4c
		###frame_c = frame_d.inverse().dot(frame_a)

		###ci_expected = frame_c.rotation*ptcloud_c.T + frame_c.displacement
		ci_a = transform(frame_a.rotation, frame_a.displacement, ptcloud_c.T)
		#ci_a = frame_a.rotation*ptcloud_c.T + frame_a.displacement
		frame_di = frame_d.inverse()
		ci_expected = transform(frame_di.rotation, frame_di.displacement, ci_a)
		#ci_expected = frame_di.rotation*ci_a + frame_di.displacement
		c_expected.append(ci_expected)
		frameAns.append(ptcloud_frame[i, 2])
	#print c_expected
	nice_c_expected = getFormat(c_expected)
	diff = nice_c_expected - np.vstack(frameAns)
	##printOutput(c_expected)
	##print nice_c_expected
	##print diff

	#Problem 5
	
	gframe = readEmpivot(empivot_fn)
	
	preEM_position = pivotCalibration(gframe)
	EM_position = preEM_position[3:6]
	#Problem 6
	optframe = readOptpivot(optpivot_fn)
	hframe = []
	#print len(optframe) #12
	for i in range(len(optframe)):
		hframe.append(optframe[i][1])
	#print hframe
	preOPT_position = pivotCalibration(hframe)
	#print preOPT_position[3:6]
	OPT_position = transform(frame_di.rotation, frame_di.displacement, preOPT_position[3:6])
	
	#print EM_position
	#print OPT_position
	output = open(output_fn, 'w')
	output.write(str(N_C) + ", " + str(N_frames) + ", " + output_fn[7:] +"\n")
	output.write(str(EM_position[0, 0]) + ",\t" + str(EM_position[1, 0]) + ",\t" + str(EM_position[2, 0]) + "\n") 
	output.write(str(OPT_position[0, 0]) + ",\t" + str(OPT_position[1, 0]) + ",\t" + str(OPT_position[2, 0]) + "\n")
	printOutput(c_expected, output)
	output.close()

	aux = open(aux_fn, 'w')
	aux.write("Differences in C_i and C_i expected\n")
	avgx = 0
	avgy = 0
	avgz = 0
	ndiff = len(diff)
	for i in range(ndiff):
		avgx += diff[i, 0]
		avgy += diff[i, 1]
		avgz += diff[i, 2]
	string = "average differences - x: %s \ty: %s \tz: %s\n" % (avgx/ndiff, avgy/ndiff, avgz/ndiff)
	aux.write(string)
	aux.write(str(diff))
	aux.close()

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

def pivotCalibration(frames):

	##print " frames: \n%s\n" % frames
	gfirst = frames[0]
	#print gfirst #6 coordinates with xyz each
	gbar = getMidpoint(gfirst)
	#print gbar # one with xyz
	ptcloud_g = gfirst - gbar
	#print ptcloud_g #6 xyz positions
	gframes = []
	#print len(frames) #12
	for i in range(len(frames)):
		gframes.append(solveFrame(ptcloud_g, frames[i]))
	disps = [] #displacements
	rotas = [] #rotations
	idens = [] #identities
	negid = -1*np.identity(3)
	for pi in gframes: #12 frames
		disps.append(-1*pi.displacement)
		rotas.append(pi.rotation)
		idens.append(negid)
	p = np.vstack(disps)
	rs = np.vstack(rotas)
	ids = np.vstack(idens)
	A = np.hstack([rs,ids])

	#ptip_dimple = ((A.T*A).I)*A.T*p
	ptip_dimple = A.I*p
	##print ptip_dimple
	return ptip_dimple


def transform(R, p, x):
	return R*x + p

def printOutput(c_expected, outfile):
	# 8 c expected's
	for c in c_expected:
		##print c.shape
		numrow, numcol = c.shape
		# 27 frames for each c
		for row in range(numcol):
			# 3 times
			outstring = ''
			for col in range(numrow):
				outstring += str(c[col, row]) + ',\t'
			outfile.write(outstring[:-2])
			outfile.write('\n')
	

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
	#from scipy import linalg as LA
	abar = getMidpoint(a)
	bbar = getMidpoint(b)

	anorm = a - abar
	bnorm = b - bbar
	matrixH = H(anorm, bnorm)	
	'''
	displace = findDisplacement(a,b).T
	print displace
	bnorm = b.T - displace
	print
	print bnorm
	matrixH = H(a, bnorm)
	'''

	matrixG = G(matrixH)
	#print matrixG
	eigvals, eigvects = LA.eig(matrixG)
	for i in range(len(eigvals)):
		maxval = max(eigvals)
		if eigvals[i] == maxval:
			maxi = i
	maxvect = eigvects[maxi]	
	#print maxi
	#print eigvals
	#print maxval
	#print maxvect	
	#print eigvects

	R = getR(maxvect)
	##print abar
	##print bbar
	displace = bbar.T - R*abar.T
	##print displace
	##print R
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
	#print len(a) #16 8's and then 12 6's but should be 24 6's from matlab... KTW
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

def readEmpivot(txt):
	import numpy as np
	from numpy import matrix

	empivot = open(txt, 'r')
	header = empivot.readline().split(',')
	N_G = int(header[0].strip())
	#print N_G #6
	N_frames = int(header[1].strip())
	empivot_fn = header[2]
	ptcloud_frame = []
	#print N_frames #12
	for j in range(N_frames):
		ptcloud_g = readCloud(empivot, N_G)
		ptcloud_frame.append(ptcloud_g)

	#return np.vstack(ptcloud_frame)
	#print ptcloud_frame #12 matrices with 6 points each
	return ptcloud_frame

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

def readOptpivot(txt):
	import numpy as np
	from numpy import matrix	
	ptcloud_frame = []

	optpivot = open(txt, 'r')
	header = optpivot.readline().split(',')
	N_D = int(header[0])
	N_H = int(header[1])
	N_frames = int(header[2])
	optpivot_fn = header[3]

	for j in range(N_frames):
		ptcloud_d = readCloud(optpivot, N_D)
		ptcloud_h = readCloud(optpivot, N_H)
		ptcloud_frame.append([ptcloud_d, ptcloud_h])

	return ptcloud_frame


if __name__ == '__main__':
    main()
