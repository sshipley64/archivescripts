#!/usr/bin/env python3
"""

requires pypyodbc module, mediainfo, VLC
2/17/2015
SJS

Usage:
	
	python cdripper.py
"""
#add vlc.exe to the path


import os
from os.path import join, getsize
import sys
import subprocess
import sma_mod
import wave

cd_files = []
ripped_files = []
cd_drive = 'D:\\'


newpath = r'K:\WorkAudio\cda_transfers\extracted_cda\temp' 
if not os.path.exists(newpath): os.makedirs(newpath)	

print("CD Ripper script")

multiplecds = 'y'
all_catalog_nums = ''

while multiplecds == 'y':
	
	while True:
	#	all_tracks = input("Should all tracks be combined into one wav file? (y or n): ")
	#	while all_tracks != "y" and all_tracks != "n":
	#			all_tracks = input("Please enter only y or n: ")
		
		catalog_num = input("Please put the CD in the CD Drive and enter the CD number: ")
		if("SMA".lower() in catalog_num.lower()):
			catalog_num = input("Please enter the number only without any prefix or characters: ")
		correct_catalog = input("You entered: " + catalog_num + ". Is this correct?(y or n): ") 
		if correct_catalog =="y":
			break
		cd_files=[]
		sma_mod.getfilelists(cd_drive, cd_files)
		print("Number of tracks on this disc: " + str(len(cd_files)))
	all_catalog_nums = all_catalog_nums + '_' + catalog_num
	
	
	size = len(cd_files)
	i =0
	while i < size:
		print("Ripping Track" + str(i+1))
		subprocess.check_call('"C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe" -I http cdda:///'+ cd_drive + ' --cdda-track='+ str(i+1)+' :sout=#transcode{acodec=s16l,channels=2}:std{access=file,mux=wav,dst=K:\\WorkAudio\\cda_transfers\\extracted_cda\\temp\\Copy_'+catalog_num + '_' + str(i+1)+'.wav} vlc://quit')
		
		i = i +1
	
	while True:
		multiplecds = input("Is there a another CD associated with this event? (y or n): ")
		if multiplecds =="y" or multiplecds =="n":
			break
		else:
			multiplecds = input(" Please enter \"y\" or \"n\": ")
	

print("Wave file is being made...")	
sma_mod.getfilelists('K:\\WorkAudio\\cda_transfers\\extracted_cda\\temp', ripped_files)
#print(ripped_files)	
outfile = "K:\\WorkAudio\\cda_transfers\\extracted_cda\\Copy"+ all_catalog_nums + ".wav"

data= []
size = len(ripped_files)
i=0
while i < size:

	w = wave.open(ripped_files[i], 'rb')
	data.append( [w.getparams(), w.readframes(w.getnframes())] )
	w.close()
	i = i + 1

output = wave.open(outfile, 'wb')
output.setparams(data[0][0])
size = len(ripped_files)
i=0
while i < size:
	output.writeframes(data[i][1])
	i = i + 1
output.close()

for ripped in ripped_files:
	os.remove(ripped)
	
	
print("The preservation wav file is complete: K:\WorkAudio\cda_transfers\extracted_cda\\Copy"+ all_catalog_nums + ".wav" )

while True:
	mp3 = input("Do you want a mp3 file made? (y or n)")
	if mp3 =="y" or mp3 =="n":
			break
	else:
		mp3 = input(" Please enter \"y\" or \"n\": ")
if mp3 == 'y':
	print("Mp3 file is being made...")	
	subprocess.check_call('"C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe" "K:\\WorkAudio\\cda_transfers\\extracted_cda\\Copy'+ all_catalog_nums +'.wav" :sout=#transcode{vcodec=none,acodec=mp3,ab=128,channels=2,samplerate=44100}:std{access=file,mux=raw,dst=K:\\WorkAudio\\cda_transfers\\extracted_cda\\Copy' + all_catalog_nums + '.mp3} vlc://quit')
print("The access mp3 file is complete: K:\WorkAudio\cda_transfers\extracted_cda\\Copy"+ all_catalog_nums + ".mp3" )			

