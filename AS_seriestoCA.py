#!/usr/bin/python
"""
CollectiveAccess API functions
"""
__author__ = "Sarah Shipley"
__version__ = "1.0"
__status__ = "Development"




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
import pymysql
import xlsxwriter


		
#r = requests.get("http://legwina114/SMA-catalog/service.php/item/ca_collections/id/98?authToken=authToken=de2a9db8e20b6971892b0531fb6f8c2d0bdec2401792dc4d4dfa558079184e80", auth=('script', '@DouglasFir1'))

#print(r.content)


#print(r.status_code)
#parsed = json.loads(r.text)
#text_output= open("E:\\CA_json_coll.txt" , "a")
#text_output.write(str(json.dumps(parsed, indent=4, sort_keys=True)))
#text_output.close()

#sql connection					
connection = pymysql.connect(host='legwarchive100',
    user='archives',
    passwd='@PacificYew1',
    db='archivesspace',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)

book = xlsxwriter.Workbook("C:\\batch\\series_update.xlsx")
sheet = book.add_worksheet('series')
#sheet.write(0, 0, 'foobar') # row, column, value
	


#Queries sql for record information
with connection.cursor() as cursor:
      
	sql = """
SELECT
a.id,
a.creatornames,
a.series,
a.title,
Case when a.begin = a.end then a.end
else CONCAT(a.begin, "-",a.end)
end as dates,
a.ead_location,


CASE
when a.extentnumber like '%;%' Then
CONCAT(SUBSTRING_INDEX (a.extentnumber, ';', -1), " ", SUBSTRING_INDEX (a.extenttype, ';', -1), " (",SUBSTRING_INDEX (a.container_summary, ';', -1),") ;",SUBSTRING_INDEX (a.extentnumber, ';', 1),  " ", SUBSTRING_INDEX (a.extenttype, ';', 1), " (",SUBSTRING_INDEX (a.container_summary, ';', 1),")")
when a.extenttype like '%digital image files%' Then
CONCAT( a.extentnumber,  " ", a.extenttype)
else CONCAT( a.extentnumber,  " ", a.extenttype , " (", a.container_summary,")")
end as extent,

CASE
when a.folderlist like '%Folder List%' then CONCAT('http://clerk.seattle.gov/~scripts/nph-brs.exe?s1=',series,'.ser.&l=50&Sect6=HITOFF&Sect5=FOLD1&Sect4=AND&Sect3=PLURON&d=FOLD&p=1&u=%2F%7Epublic%2Ffold1.htm&r=0&f=S')
else ''
end as folderlink,
SUBSTRING_INDEX (SUBSTRING_INDEX (a.scopenote, ',"content":"', -1), '","', 1) as scopenote,
SUBSTRING_INDEX (SUBSTRING_INDEX (a.GRUP, ',"content":"', -1), '","', 1) as recordgroup,
a.corporate_name,
a.personal_name


FROM archivesspace.brs_sers_output a left join archivesspace.resource b on a.id = b.id
where b.user_mtime > subdate(current_date, 3)
"""
	cursor.execute(sql, )
	result = cursor.fetchall()
	#puts results in lists
	i=1
	for row in result:
		sheet.write(i, 0, row['id'])
		sheet.write(i, 1, row['creatornames'])
		sheet.write(i, 2, str(row['series']).replace("\n","<br />").replace("\n","<br />").replace("\n","<br />"))
		sheet.write(i, 3, row['title'])
		sheet.write(i, 4, row['dates'])
		sheet.write(i, 5, row['ead_location'])
		sheet.write(i, 6, row['extent'])
		sheet.write(i, 7, row['folderlink'])
		sheet.write(i, 8, str(row['scopenote']).replace("\\n","<br />").replace("\\n","<br />").replace("\\n","<br />"))
		sheet.write(i, 9, row['recordgroup'])
		sheet.write(i, 10, row['corporate_name'])
		sheet.write(i, 11, row['personal_name'])
		i+=1

	book.close()
#input = input("chcha")


#payload = {'username': 'bob', 'email': 'bob@bob.com'}
#r = requests.put("http://somedomain.org/endpoint", data=payload)
#
#r.content





