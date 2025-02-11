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
import xlsxwriter


connection_AS = pymysql.connect(host='legwarchive100',
    user='root',
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

	with connection.cursor() as cursor:
		sql = 	"""
		SELECT b.row_id, h.idno as objectidno,c.value_longtext1 as box, d.value_longtext1 as folder, i.value_longtext1 as item, g.idno  FROM collectiveaccess175prep.ca_attribute_values a left join `collectiveaccess175prep`.`ca_attributes` b on a.attribute_id = b.attribute_id
		left join `collectiveaccess175prep`.`ca_objects`h on b.row_id = h.object_id
		left join collectiveaccess175prep.ca_attribute_values c on a.attribute_id = c.attribute_id
        left join collectiveaccess175prep.ca_attribute_values d on a.attribute_id = d.attribute_id
         left join collectiveaccess175prep.ca_attribute_values e on a.attribute_id = e.attribute_id
		   left join collectiveaccess175prep.ca_attribute_values i on a.attribute_id = i.attribute_id
        left join `collectiveaccess175prep`.`ca_objects_x_collections` f on b.row_id = f.object_id
         left join `collectiveaccess175prep`.`ca_collections` g on f.collection_id = g.collection_id
         
        where b.table_num = 57
        and a.element_id =174
        and c.element_id =172
        and c.value_longtext1 is not null
        and d.element_id =173
		  and i.element_id =176
        and d.value_longtext1 is not null
        and e.element_id=305
        and e.value_longtext1 is null
        and g.type_id =116
		and (h.type_id = 25 or h.type_id = 23)
        and h.deleted =0
		"""
		 
		db_cursor.execute(sql)
		rows = db_cursor.fetchall()
		
		for row in rows:
			object_id.append(row['row_id'])
			idnos.append(row['objectidno'])
			box_value.append(row['box'])
			items.append(row['item'])
			foldervalue.append(row['folder'])
			series.append(row['idno'])
			
			
		
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
		with connection_AS.cursor() as cursor:
			sql = 	"""
			SELECT id FROM archivesspace.brsfold_basic6 where series = %s and indicator_1 = %s;
			"""
			 
			cursor.execute(sql, (series,indicator,))
			#print("SQL output tables built and populated")
			result2 = cursor.fetchone()['id']
			cursor.close()
	except:
		result2="None"
	return result2		
	
def create_identifiers():	
		
	with connection_AS.cursor() as cursor:
		sql = 	"""
		CALL `archivesspace`.`create_identifiers`();

		"""
			 
		cursor.execute(sql,)
		#print("SQL output tables built and populated")
			
	
	
def gettitle(series,indicator):	
		
	try:
		with connection_AS.cursor() as cursor:
			sql = 	"""
			SELECT title FROM archivesspace.brsfold_basic6 where series = %s and indicator_1 = %s;
			"""
			 
			cursor.execute(sql, (series,indicator,))
			#print("SQL output tables built and populated")
			result2 = cursor.fetchone()['title']
			cursor.close()
	except:
		result2="None"
	return result2
def getdates(series,indicator):	
		
	try:
		with connection_AS.cursor() as cursor:
			sql = 	"""
			SELECT IF (`begin` = `end` ,`begin`, Concat(`begin`,'-',`end`) ) as dates FROM archivesspace.brsfold_basic6 where series = %s and indicator_1 = %s;
			"""
			 
			cursor.execute(sql, (series,indicator,))
			#print("SQL output tables built and populated")
			result2 = cursor.fetchone()['dates']
			cursor.close()
	except:
		result2="None"
	return result2
		
object_id =[]
foldervalue =[]
box_value =[]
series=[]
as_id =[]
idnos=[]
items=[]

create_identifiers()

update = "C:\\batch\\folderlink_update.xlsx"
if os.path.exists(update):
	os.remove(update)
book = xlsxwriter.Workbook("C:\\batch\\folderlink_update.xlsx")
sheet = book.add_worksheet('folderlink')


get_object_folders()
i=0
size = len(object_id)
while i <size:
	print(object_id[i])
	print(box_value[i])
	print(foldervalue[i])
	print(series[i])
	break
	i+=1

	

new_idnos=[]
new_dates=[]
new_title=[]
new_box=[]
new_folder=[]
new_items=[]




i=0
size = len(object_id)
while i <size:
	
	try:
		as_link= getidnumber(series[i],str(box_value[i])+"/"+str(foldervalue[i]))
		if str(as_link) != "None":
		
			as_id.append(as_link)
			new_idnos.append(idnos[i])
			if getdates(series[i],str(box_value[i])+"/"+str(foldervalue[i])) == None:
				date=""
			else:
				date=getdates(series[i],str(box_value[i])+"/"+str(foldervalue[i]))
			new_dates.append(date)
			new_title.append(gettitle(series[i],str(box_value[i])+"/"+str(foldervalue[i])))
			new_box.append(box_value[i])
			new_folder.append(foldervalue[i])
			if items[i] == None or items[i] =="None":
				new_items.append("")
			else:
				new_items.append(items[i])
			
		
	except:
		pass
	
	i+=1
print(as_id[0])


size = len(new_idnos)
i=0
while i<size:
	sheet.write(i, 0, new_idnos[i])
	sheet.write(i, 1, "http://archives.seattle.gov/finding-aids/repositories/2/archival_objects/"+str(as_id[i]))
	sheet.write(i, 2, str(new_box[i]))
	sheet.write(i, 3, str(new_folder[i]))
	sheet.write(i, 4, str(new_title[i]))
	sheet.write(i, 5, str(new_dates[i]))
	sheet.write(i, 6, str(new_items[i]))
	i+=1

book.close()

