'''
	@author: 00933557 / Manjunatha
	@created on: 3/22/2020
	
	@Description: This script 
	1. renames DNP_SUPPRESSION_MMDDYY_HHMMSS.csv to DNP_SUPPRESSION.csv
	2. connects to Eloqua and archives last week's file
	3. moves a new file BODS FTP server to Eloqua SFTP server
'''
00222786 - who is this?
import paramiko, datetime, os
from glob import glob

username = "MktgcFTP"
port = 22
remotepath = "/MktgcFTP/to_MktgcFTP/DNP_SUPPRESSION.csv"
localpath = os.getcwd()
print(localpath + '\DNP_SUPPRESSION.csv')

try:
	filename = glob(os.path.join(localpath,"DNP_SUPPRESSION*"))[0]
	os.rename(filename, os.path.join(localpath,"DNP_SUPPRESSION.csv"))
	print('File ' + filename + ' renamed to DNP_SUPPRESSION.csv')
	
	t = paramiko.Transport(('ftp1.centerpointenergy.com', port))
	t.connect(username=username, password='pjFKNq5H')
	sftp = paramiko.SFTPClient.from_transport(t)
	print('Connection Success to Eloqua')
	
	print('Archiving Last Week\'s File')
	sftp.chdir(path='/MktgcFTP/to_MktgcFTP')
	mtime = sftp.stat('/MktgcFTP/to_MktgcFTP/DNP_SUPPRESSION.csv').st_mtime
	dt_object = datetime.datetime.fromtimestamp(mtime)
	archive_filename = 'DNP_SUPPRESSION_' + dt_object.strftime('%m%d%Y_%H%M%S') + '.csv'
	sftp.rename('/MktgcFTP/to_MktgcFTP/DNP_SUPPRESSION.csv', '/MktgcFTP/from_MktgcFTP/Archive/'+archive_filename)
	print('File: /MktgcFTP/to_MktgcFTP/DNP_SUPPRESSION.csv successfully archived to '+ '/MktgcFTP/from_MktgcFTP/Archive/'+archive_filename)
	
	sftp.put(localpath + '\DNP_SUPPRESSION.csv', remotepath, callback=None, confirm=False)
	print('New file moved to Eloqua')
except Exception as e:
	print("Something went wrong! Please review python script")
	print(traceback.format_exc())
finally:
    t.close()
	

