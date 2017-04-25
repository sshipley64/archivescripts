#!/usr/bin/python
"""
ArchivesSpace adding file level box-folders. 
USE at your own risk....

"""
__author__ = "Sarah Shipley"
__version__ = "1.3"





import os
import sys
import time
from time import strftime
import datetime
from datetime import datetime, timedelta

import json
import shutil
import requests
import csv


#AS backend  ADD your own information here
backendURL ='http://localhost:8089'
user ='admin'
pw = 'admin'
repoID = '2'


	


def readitemcsv(filename):
	'''
	Takes reads the first column from an Excel created csv file and puts it into a python list
	The csv file should have no header. 
	'''
	with open(filename, newline='') as f:
		rows = csv.reader(f, delimiter=',')
		try:
			for row in rows:
				for index, field in enumerate(row):
					if index == 0:
						box.append(field)
					if index == 1:
						folder.append(field)
					if index == 2:
						folder_title.append(field.strip())
					if index == 3:
						date_type.append(field)
					if index == 4:
						date_label.append(field)
					if index == 5:
						date_begin.append(field.strip())
					if index == 6:
						date_end.append(field.strip())
					if index == 7:
						date_expression.append(field.strip())
					if index == 8:
						general_label.append(field)
					if index == 9:
						general_content.append(field)
					
						
		except csv.Error as e:
			sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))

connectASpace = requests.post(backendURL + "/users/" + user + "/login", data = {"password":pw})
	
#print(connectASpace.status_code)
if connectASpace.status_code == 200:
	print ("Connection Successful")
else: 
	print('No AS Connection')
#print(connectASpace.content)

sessionID = connectASpace.json()["session"]
headers = {'X-ArchivesSpace-Session': sessionID}
#print(sessionID)
			
			
box =[]
folder = []
folder_title =[]
dates =[]	
date_type =[]
date_label =[]
date_begin =[]
date_end =[]
date_expression =[]
general_label =[]
general_content =[]



archival_object_id = ""


#User input section 
print("File level upload to AS script--for versions 1.5 -2.0")
filepath= input("Enter the file path of the csv file of your file level records: (ex. C:\\csvfolder\\MyASFiles.csv)")

if os.path.exists(filepath):
	print("\nYou have entered:",filepath)
else:
	sys.exit(filepath+" can't be found. Please rerun script with correct path.")
resource_id = input("\nPlease enter the AS id number for the root resource \n(Look at the number in the url on the resource page ex.1520 in  http://localhost:8080/resources/1520/: ")
while True:
		archival_object_exists = input("\nShould the files be entered under an archival object (series, subseries under a resource? (y or n)")
		if archival_object_exists == "y":
			archival_object_id = input("\nPlease enter the archival_object_id \n(Look at the last number in the url when the ao is selected. ex.171270 in  http://localhost:8080/resources/1520/edit#tree::archival_object_171270) :\n")
			break
		if archival_object_exists == "n":
			break
		else:
			archival_object_exists = input(" Please enter \"y\" or \"n\": ")

backup= input("\nA backup EAD called "+str(resource_id)+".xml of this resource will be created. \n Enter the folder path where it should be created: (ex. C:\\mybackupead)")
#user input end

#create a backup ead
ead = requests.get(backendURL + '/repositories/'+repoID+'/resource_descriptions/'+str(resource_id)+'.xml', headers=headers).text
print(ead)
		# Sets the location where the files should be saved
destination = backup
f = open(destination+"\\"+str(resource_id)+'.xml', 'a')
f.write(ead)
f.close
print (str(resource_id)+ ' exported to ' + destination)



#read csv file
readitemcsv(filepath)	

	
#add files to parent record
print("\nThere are ",len(box)-1," file records.\n")


size =len(box)
i=1
while i<size:


	parsed = { "jsonmodel_type":"archival_object",
	"external_ids":[],
	"subjects":[],
	"linked_events":[],
	"extents":[],
	"dates": [
			{
				"begin": date_begin[i],
			  
				"date_type": date_type[i],
				"end": date_end[i],
				"expression": date_expression[i],
				"jsonmodel_type": "date",
				"label": date_label[i],
				"lock_version": 0,
			   
			}
		],
	"external_documents":[],
	"rights_statements":[],
	"linked_agents":[],


	"instances": [
			{
				"container": {
					"container_locations": [],
					"indicator_1": box[i],
					
					"lock_version": 9,
					"type_1": "box",
					"type_2": "folder",
					"indicator_2": folder[i],
				},
		  
				"instance_type": "mixed_materials",
			   
				"jsonmodel_type": "instance",
			
				"lock_version": 0,
			   
			
			}
		],

	"notes": [],


	"lock_version": 1,
	"level":"file",
	"title":folder_title[i],
	
	"resource":{ "ref":"/repositories/"+repoID+"/resources/"+resource_id},
	"parent": { 
		"ref": ""
			
		},
	"publish": True,
	}

	#add parent if needed
	if archival_object_id != "":
		parsed['parent']['ref']= "/repositories/"+repoID+"/archival_objects/"+archival_object_id
		
	
	#add note if needed
	if general_content[i] != None:
		parsed['notes'].append({
				"jsonmodel_type": "note_multipart",
				"label": general_label[i],
				"publish": True,
				"subnotes": [
					{
						"content": general_content[i],
						"jsonmodel_type": "note_text",
						"publish": True
					}
				],
				"type": "odd"
			})
	
		
	
	print(backendURL + "/repositories/:" + repoID + "/archival_objects")
	ingested_json=requests.post(backendURL + "/repositories/" + repoID + "/archival_objects", headers=headers, json=parsed)

	print(ingested_json.status_code)
	print(ingested_json.content)


	
	i=i+1

print("Script finished.")


