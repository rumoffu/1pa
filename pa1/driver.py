#!/usr/bin/env python
"""
@author Deepak Lingam and Kyle Wong
This is a driver program to run a Point Cloud to Point Cloud Registration
and a Pivot Calibration.
"""
#import matplotlib.pyplot as plt  
import numpy as np 


def main():
"Program to open a data set
 and do a point cloud to point cloud registration"
	#open data set
	readCalbody("../input_data/pa1-debug-a-calbody.txt")

def readCalbody(txt):
	calbody = open(txt, 'r')
	

if __name__ == '__main__':
    main()
