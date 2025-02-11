C:\Python34\python.exe C:\batch\AS_seriestoCA.py
C:\Python34\python.exe C:\batch\AStoCA.py
C:\Python34\python.exe C:\batch\CAtoAS-custom.py
D:
cd D:\SMA-catalog\support
php bin/caUtils load-import-mapping --file=C:\batch\series_map.xlsx
php bin/caUtils import-data --format=XLSX --mapping=series_map --source=C:\batch\series_update.xlsx --log=D:\logs\series_update_log.txt
php bin/caUtils load-import-mapping --file=C:\batch\folder_link.xlsx
php bin/caUtils import-data --format=XLSX --mapping=folder_link --source=C:\batch\folderlink_update.xlsx --log=D:\logs\folderlink_update_log.txt
C:\Python34\python.exe C:\batch\CAtoAS.py
