#!/usr/bin/python
"""
Add electronic copy note to AS if text record is modified in CA to include a series, box and folder. 

Sarah Shipley

Usage:
	
	python putPhotos.py
	
"""
__author__ = "Sarah Shipley"
__version__ = "1.0"
__status__ = "Development"

import sys




import os
import re


import time
import getpass
import pymysql
import json
import shutil


import subprocess

import os
import sys
import getpass
import time
from time import strftime
import datetime
from datetime import datetime, timedelta


import json
import shutil
import requests


connectionAS = pymysql.connect(host='legwarchive100',
    user='archives',
    passwd='@PacificYew1',
    db='archivesspace',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)

#AS backend
backendURL ='http://legwarchive100:8089'
user ='scripts'
pw = '@PacificYew1'
connectASpace = requests.post(backendURL + "/users/" + user + "/login", data = {"password":pw})
	
print(connectASpace.status_code)
if connectASpace.status_code == 200:
	print ("Connection Successful")
else: 
	print('No AS Connection')


sessionID = connectASpace.json()["session"]
headers = {'X-ArchivesSpace-Session': sessionID}
repoID= '2'	



connection = pymysql.connect(host='legwina114',
    user='archives',
    passwd='@DouglasFir1',
    db='collectiveaccess175prep',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)
	
db_cursor = connection.cursor()	

def get_object_folders():	
	print("getting object folders")
	with connection.cursor() as cursor:
		sql = 	"""
		SELECT b.row_id, a.value_longtext1, date_format(from_unixtime(c.log_datetime),'%Y%m%d') FROM collectiveaccess175prep.ca_attribute_values a left join `collectiveaccess175prep`.`ca_attributes` b on a.attribute_id = b.attribute_id
		left join  `collectiveaccess175prep`.`ca_change_log` c on b.row_id = c.logged_row_id
        left join   `collectiveaccess175prep`.`ca_objects`d on b.row_id = d.object_id
        where a.element_id =173 and d.deleted = 0 and b.table_num = 57 and a.value_longtext1 is not null and date_format(from_unixtime(c.log_datetime),'%Y%m%d') > DATE(NOW() - INTERVAL 90 DAY) 
		"""
		 
		db_cursor.execute(sql)
		rows = db_cursor.fetchall()
		
		for row in rows:
			object_id.append(row['row_id'])
			foldervalue.append(row['value_longtext1'])
			
		
def get_object_box(object_id):	
	
	boxvalue =""
	with connection.cursor() as cursor:
		sql = 	"""
		SELECT  a.value_longtext1  FROM collectiveaccess175prep.ca_attribute_values a left join `collectiveaccess175prep`.`ca_attributes` b on a.attribute_id = b.attribute_id

		where a.element_id =172  and a.value_longtext1  is not null and b.row_id = %s
		"""
		 
		db_cursor.execute(sql, str(object_id))
		rows = db_cursor.fetchall()
		
		for row in rows:
			boxvalue = row['value_longtext1']
			
	return boxvalue
	
def get_series(object_id):	
	
	series =""
	with connection.cursor() as cursor:
		sql = 	"""
		SELECT b.idno FROM collectiveaccess175prep.ca_objects_x_collections a left join `collectiveaccess175prep`.`ca_collections` b on a.collection_id = b.collection_id
		where a.object_id = %s limit 1
		"""
		 
		db_cursor.execute(sql, str(object_id))
		rows = db_cursor.fetchall()
		
		for row in rows:
			series = row['idno']
			
	return series
	
	
	
	
def get_all_series_dropdown():	
	idno =[]
	name =[]	
	dropdown = "D:\\SMA-catalog\\digital-collections\\media\\series_dropdown.xml"
	if os.path.exists(dropdown):
		os.remove(dropdown)
	output =open(dropdown , "a")
	output.write('<?xml version="1.0" encoding="utf-8"?><bodyname>')
	
	with connection.cursor() as cursor:
		sql = 	"""
		SELECT DISTINCT a.idno, d.name FROM collectiveaccess175prep.ca_collections a join collectiveaccess175prep.ca_objects_x_collections b on a.collection_id = b.collection_id
		join collectiveaccess175prep.ca_objects c on b.object_id = c.object_id
		join collectiveaccess175prep.ca_collection_labels d on a.collection_id = d.collection_id
		where a.access =1 and c.deleted=0 and c.access =1 order by a.idno
		"""
		 
		db_cursor.execute(sql)
		rows = db_cursor.fetchall()
		
		for row in rows:
			idno.append(row['idno'])
			name.append(row['name'])
			
		i=0
		size =len(idno)
		while i < size:
			output.write('<p id="'+idno[i]+'" nm="'+name[i].strip("\r\n")+ '"/>\n')
			i=i+1
		output.write('</bodyname>')
		output.close()

def get_series_dropdown(type_id, prefix):	
	idno =[]
	name =[]	
	dropdown = "D:\\SMA-catalog\\digital-collections\\media\\"+str(prefix)+"_series_dropdown.xml"
	if os.path.exists(dropdown):
		os.remove(dropdown)
	output =open(dropdown , "a")
	output.write('<?xml version="1.0" encoding="utf-8"?><bodyname>')
	
	with connection.cursor() as cursor:
		sql = 	"""
		SELECT DISTINCT a.idno, d.name FROM collectiveaccess175prep.ca_collections a join collectiveaccess175prep.ca_objects_x_collections b on a.collection_id = b.collection_id
		join collectiveaccess175prep.ca_objects c on b.object_id = c.object_id
		join collectiveaccess175prep.ca_collection_labels d on a.collection_id = d.collection_id
		where a.access =1 and c.type_id=%s and c.deleted=0 and c.access =1 order by a.idno
		"""
		 
		db_cursor.execute(sql,type_id)
		rows = db_cursor.fetchall()
		
		for row in rows:
			idno.append(row['idno'])
			name.append(row['name'])
			
		i=0
		size =len(idno)
		while i < size:
			output.write('<p id="'+idno[i]+'" nm="'+name[i].strip("\r\n")+ '"/>\n')
			i=i+1
		output.write('</bodyname>')
		output.close()

def get_subject_typeahead():
	name_singular =[]
	typeahead = "D:\\SMA-catalog\\digital-collections\\media\\subjectterms.txt"
	if os.path.exists(typeahead):
		os.remove(typeahead)
	output =open(typeahead , "a")
	with connection.cursor() as cursor:
		sql ="""
		SELECT DISTINCT b.name_singular
		FROM collectiveaccess175prep.ca_attribute_values a join collectiveaccess175prep.ca_list_item_labels b on a.item_id = b.item_id
		where a.element_id = 72 order by b.name_singular;
		"""
		db_cursor.execute(sql,type_id)
		rows = db_cursor.fetchall()
		
		for row in rows:
			name_singular.append(row['name_singular'])
			
			
		i=0
		size =len(name_singular)
		while i < size:
			output.write(name_singular[i]+'\n')
			i=i+1
		
		output.close()
		
def getidnumber(series,indicator):	
		
	try:
		with connectionAS.cursor() as cursor:
			sql = 	"""
			SELECT id FROM archivesspace.basic6 where series = %s and indicator_1 = %s;
			"""
			 
			cursor.execute(sql, (series,indicator))
			#print("SQL output tables built and populated")
			result2 = cursor.fetchone()['id']
			cursor.close()
	except:
		print("Nope")
		result2="None"
	return result2		
		
object_id =[]
foldervalue =[]
box_value =[]
series=[]
as_id =[]

get_object_folders()
i=0
size = len(object_id)
objects2  =[]
print(object_id)
#stop= input("stop")
while i <size:
	print(i)
	if str(get_series(object_id[i])) != '1802-04':
		box_value.append(get_object_box(object_id[i]))	
		series.append(get_series(object_id[i]))
		objects2.append(object_id[i])       
	i+=1

	

	


i=0

size = len(objects2)
print(size)
while i <size:
    print(i)
    print(series[i])
    print(str(box_value[i])+"/"+str(foldervalue[i]))
    try:
        as_id.append(getidnumber(series[i],str(box_value[i])+"/"+str(foldervalue[i])))
    except:
        print("No")
        input = input("Stop")
        as_id.append("")
    i+=1
	
i=0

while i < len(objects2):
	print(i)
	print(str(series[i]) + " "+ str(box_value[i])+ " "+ str(foldervalue[i])+ " "+str(as_id[i]))
		
	archival_object = requests.get(backendURL + "/repositories/" + repoID + "/archival_objects/" + str(as_id[i]),  headers=headers)
	prefix = "https://archives.seattle.gov/digital-collections/index.php/Search/objects/search/ca_objects.type_id%3A25+AND+ca_collections.idno%3A+%22"
	middle = "%22+AND+ca_objects.location.folder_num%3A%22"
	middle2 = "%22+AND+ca_objects.location.loc_box%3A%22"
	suffix = "%22"
			
	link = prefix + str(series[i]) + middle + str(foldervalue[i]) + middle2 + str(box_value[i]) + suffix
	print(link)
	print(backendURL + "/repositories/" + repoID + "/archival_objects/"  + str(as_id[i]))
	if "error" in archival_object.text:
		pass
	else:
		parsed = json.loads(archival_object.text)
		z=0
		while z <len(parsed['notes']):
			#print(note)
			if "Electronic Copy" in str(parsed['notes'][z]):
				print("Yes")
				parsed['notes'].remove(parsed['notes'][z])
				
			z+=1
		#print("aNd now"+ str(parsed['notes']))
		#print(parsed['notes'][0])
		parsed['notes'].append({
					"jsonmodel_type": "note_multipart",
					"label": "Electronic Copy",
				   
					"publish": True,
					"subnotes": [
						{
							"content": link,
							"jsonmodel_type": "note_text",
							"publish": True
						}
					],
					"type": "odd"
				})

		#text_output= open("C:\\batch\\AS_json_archival_object.txt" , "a")
		#text_output.write(str(json.dumps(parsed, indent=4, sort_keys=True)))
		#text_output.close()

		backendURL + "/repositories/" + repoID + "/archival_objects/" + str(as_id[i])

		ingested_json=requests.post(backendURL + "/repositories/" + repoID + "/archival_objects/" + str(as_id[i]), headers=headers, json=parsed)
		print(ingested_json.status_code)
		print(ingested_json.content)
		#if "error" in ingested_json.content:
		#	text_output= open("C:\\batch\\AS_link_error.txt" , "a")
		#	error = str(str(series[i]) + " "+ str(box_value[i])+ " "+ str(foldervalue[i]))
		#	text_output.write(error.encode())
				
	i+=1