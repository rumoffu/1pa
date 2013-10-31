/**
Kyle Wong and Deepak Lingam
README.TXT
**/

List of programs:
driver.py

Directions:
In order to use our program without any problems, we wish that you use a Linux operating system. In addition, in order to change the input files, you will need to go into our source code and change the file names at the top of the program.

If you would like to set the input file, you can open driver.py and edit the prefix:
for example, to use pa1-debug-a-calbody.txt, simply edit it to be:
prefix = "pa1-debug-a"

Then, the code can be run using
python driver.py

Alternatively, you can set the permission to make the file executable and then run it as
./driver.py

On linux, you can set the permission by doing chmod +x driver.py


Directory listing:
driver.py - the main file containing the methods for reading in the input data, solving the frame transformations, doing the point cloud registrations, and doing the pivot calibration

