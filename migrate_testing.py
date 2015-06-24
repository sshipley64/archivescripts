#!/usr/bin/env python3
"""Testing for migration from export files
Compares files line by line, discounting white space, pauses and displays differences
used to compare exported and formatted load files from migrated system to the original

6/16/2015
SJS

Usage:
	
	python migrate_testing.py
"""

import time
from time import gmtime, strftime
import math
import os
from os.path import join, getsize
import getpass
import subprocess


import ctypes
import platform
import re
import sys
import csv
import json
import pymysql

origline = []
#first file
f = open('C:\\testingfolder\\brsfoldload.txt')
for line in iter(f):
	origline.append(line.strip())	
f.close()
print("finished original ingest")
newline = []
#comparison file
f = open('C:\\testingfolder\\brsfoldload_as.txt')
for line in iter(f):
	newline.append(line.strip())	
f.close()
print("finished new ingest")
size = len(origline)
i= 0
while i < size:
	if origline[i].lower() != newline[i].lower():
		print( str(i) + "\nold line: " + origline[i] + "\nnew line: " + newline[i])
		contin = input("continue?")
	else:
		print(str(i))
	i= i + 1
