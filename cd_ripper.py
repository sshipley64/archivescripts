#!/usr/bin/env python3
"""
For legacy audio divided up into cda tracks on CD
Takes all tracks on the cd and combines together into a wav file named Copy_####
This can then be used with the audio script to automate the cataloging of the wav file. 


requires VLC
2/17/2015
SJS

Usage:
	
	python cdripper.py
"""
#add vlc.exe to the path variable
#vlc "cdda:// Audio CD - Track 01" --sout=#transcode{acodec=s16l,channels=2}:std{access=file,mux=wav,dst=C:\testingfolder\mytestingfile4.wav} vlc://quit
#vlc K:\WorkAudio\cda_transfers\extracted_cda\Copy_14909.wav --sout=#transcode{acodec=mp3,ab=128,channels=2}:std{access=file,mux=mp3,dst=C:\testingfolder\mytestingfile5.mp3} vlc://quit


import os
from os.path import join, getsize
import sys
import subprocess

location = "K:\WorkAudio\cda_transfers\extracted_cda"

while True:

	catalog_num = input("Enter the the CD number: ")
	if("SMA".lower() in catalog_num.lower()) or ("Copy".lower() in catalog_num.lower()):
		catalog_num = input("Please enter the number only without any prefix or characters: ")
	correct_catalog = input("You entered: " + catalog_num + ". Is this correct?(y or n): ") 
	if correct_catalog =="y":
		break

		

subprocess.check_call('vlc.exe "cdda://" --sout=#transcode{acodec=s16l,channels=2}:std{access=file,mux=wav,dst=' + location + '\Copy_' + catalog_num + ".wav} vlc://quit")
print("The preservation wav file is complete and can be found in " + location )
	
