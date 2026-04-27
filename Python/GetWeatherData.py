from ftplib import FTP
from datetime import datetime
import sys, os, gzip, shutil
import traceback, logging

def get_weather_data(dir): # Get weather files from NOAA for a set of stations
	counter = 0
	day_num = datetime.now().timetuple().tm_yday
	year = datetime.now().year
	stations = ["722543-12977-", "722436-12906-", "722430-12960-", "722420-12923-", "722429-53910-", "722440-12918-", "722427-12975-", "722527-12976-"]
	try:
		print('Downloading files from NOAA...')
		ftp = FTP("ftp.ncdc.noaa.gov")
		ftp.login()
		ftp.cwd('/pub/data/noaa/isd-lite/'+ str(year))
		if day_num <= 61:
			year = year-1
			ftp.cwd('/pub/data/noaa/isd-lite/'+ str(year))
		for s in stations:
			filename = s+str(year)+'.gz'
			with open(dir+filename, 'wb') as fp:
				ftp.retrbinary('RETR '+filename, fp.write)
				counter += 1
				print("Retrieved File: " + filename)
		ftp.close()
		if counter == 0:
			raise Exception("Sorry, no files downloaded!")
			logging.error("NO_FILES_EXCEPTION")
			logging.error(traceback.format_exc())
		else:
			print("Downloads completed successfully: Retrieved " + str(counter) + " files")
	except Exception as e:
		logging.error("get_weather_data() failed!!!")
		logging.error(traceback.format_exc())

def get_all_zip_files(dir, extension='.gz'): # Get a list files with .gz extension
	gzfiles = []
	try:
		for root, dirs, files in os.walk(dir):
			for file in files:
				ext = os.path.splitext(file)[-1].lower()
				if ext == extension:
					gzfiles.append(os.path.join(root, file))
		return gzfiles
	except Exception as e:
		logging.error("get_all_zip_files() failed!!!")
		logging.error(traceback.format_exc())
		
def gunzip(source, dest, block_size=65536):
    with gzip.open(source, 'rb') as s_file, open(dest, 'wb') as d_file:
        shutil.copyfileobj(s_file, d_file, block_size)

def transform_weather_files(dir): # Extract .gz files into .txt files
	'''
	# remove all the files in directory \ISASSTG\Weather\
	print('Removing old files in \ISASSTG\Weather')
	for root, dirs, files in os.walk(dir):
		for file in files:
			os.remove(os.path.join(root, file))
	print('Old files removed')
	'''
	# fetch new files to directory \ISASSTG\Weather\ from NOAA
	get_weather_data(dir)
	
	# get list of files with .gz extension
	gzfiles = get_all_zip_files(dir)
	
	# start files decompression
	try:
		print('Starting files decompression...')
		for gzfile in gzfiles:
			txtfile = os.path.basename(gzfile)[:-3] + '.txt'
			gunzip(gzfile, dir+txtfile)
			print(dir+txtfile)
		print('Files have been decompressed')
	except Exception as e:
		logging.error("transform_weather_files() failed!!!")
		logging.error(traceback.format_exc())
	
if __name__ == "__main__":
	#save_to = "D:\\BO_LANDING_ZONE\\ISASSTG\\Weather\\"
	save_to = "C:\\Users\\manjunatha.k\\Desktop\\"
	transform_weather_files(save_to)
