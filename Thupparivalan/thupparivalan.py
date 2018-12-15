import os
import difflib
from apiclient.discovery import build  # pip install google-api-python-client
import io
from apiclient.http import MediaIoBaseDownload
import datetime
import ConfigParser

#Check the Configuration and set the required variables
if os.path.exists("thuppu.config"):
	config = ConfigParser.RawConfigParser()
	config.read('thuppu.config')
	try:
		if config.get('SETTINGS', 'PARENT_FOLDER_NAME')== "":
			print "\nParent folder name not set to monitor. Set it in config before running !!"
			os._exit(1)
		if config.get('SETTINGS', 'PARENT_FOLDER_ID') == "":
			print "\nThe set PARENT_FOLDER_ID in thuppu.config file seems invalid. \n\nFor how to's of  finding folder ID  go to :- \n\"https://googleappsscriptdeveloper.wordpress.com/2017/03/04/how-to-find-your-google-drive-folder-id/\""
			os._exit(1)
		if config.get('SETTINGS', 'SECRET_CREDENTIAL_JSON') == "":
			raise Exception
		if config.get('SETTINGS', 'SECRET_TOKEN_JSON') =="":
			raise Exception
	except:
		print "\nCorrupted thuppu.config File!! Thupparivalan cannot run!!"
		os._exit(1)
		
else:
	print "\nConfiguration File thuppu.config not found in path!! Thupparivalan cannot run!!"
	os._exit(1)

#Check for OS for deciding on path character
if os.name == "nt":
	path_char="\\"
else:
	path_char="/"

if os.path.exists("credentials.json"):
	pass
else:
	print "\nSecret Credentials \"credentials.json\" file not found in the current directory.\nStep 1: Go to https://developers.google.com/drive/api/v3/quickstart/python \nStep 2: Follow till all steps within  \"Step 1: Turn on the Drive API\". \nStep 3: Copy the downloaded credentials.json in the same folder as thupparivalan and run !!"
	os._exit(1)

def get_credentials(scopes, secrets=config.get('SETTINGS', 'SECRET_CREDENTIAL_JSON'), storage=config.get('SETTINGS', 'SECRET_TOKEN_JSON')):
	from oauth2client import file, client, tools
	store = file.Storage(os.path.expanduser(storage))
	creds = store.get()
	if creds is None or creds.invalid:
		flow = client.flow_from_clientsecrets(os.path.expanduser(secrets), scopes)
		creds = tools.run_flow(flow, store)
	return creds


def iter_folder(id=None,parent_path=None,currentstate=None):
	q = []
	q.append("'%s' in parents" % id.replace("'", "\\'"))
	q.append("trashed=false")
	
	params = {'pageToken': None, 'fields' : 'files(id,name,createdTime,modifiedTime,mimeType)', 'orderBy':'name'}
	params['q'] = ' and '.join(q)
	
	response = service.files().list(**params).execute()
	while True:
		response = service.files().list(**params).execute()
		for f in response['files']:
			print parent_path+f['name']+"  "+f['modifiedTime']
			currentstate.write(parent_path+f['name']+"`"+f['mimeType']+"`"+f['createdTime']+"`"+f['modifiedTime']+"`"+f['id']+"\n")
			iter_folder(id=f['id'],parent_path=parent_path+f['name']+path_char,currentstate=currentstate)
		try:
			params['pageToken'] = response['nextPageToken']
		except KeyError:
			return


def finding_diff(previousstate=None,currentstate=None):
	changes=[] #[('+',id,pat,folder or file )] +=created , -=deletec, ^=modified
	diff=difflib.ndiff(sorted(previousstate),sorted(currentstate))
	delta=''.join(diff)
	tempminus=[]
	tempplus=[]
	for i in delta.split("\n"):
		if i.startswith("- "):
			tempminus.append(i)
		if i.startswith("+ "):
			tempplus.append(i)
	if len(tempminus) ==0 and len(tempplus)==0:
		print "No changes from last time."
		return
	for count1 in range(len(tempminus)):
		modflag=0
		createflag=1
		for count2 in range(len(tempplus)):
			# Checking for Modification
			if tempminus[count1].split("`")[4]==tempplus[count2].split("`")[4]:
				modflag=1
				if tempminus[count1].split("`")[0].__getslice__(2,len(tempminus[count1].split("`")[0]))== tempplus[count2].split("`")[0].__getslice__(2,len(tempplus[count2].split("`")[0])):
					print tempplus[count2].split("`")[0].__getslice__(2,len(tempplus[count2].split("`")[0])) + " has been modified"
				else:
					print tempminus[count1].split("`")[0].__getslice__(2,len(tempminus[count1].split("`")[0])) + " modified to "+tempplus[count2].split("`")[0].__getslice__(2,len(tempplus[count2].split("`")[0]))
				changes.append(('^',tempplus[count2].split("`")[4],tempplus[count2].split("`")[0].__getslice__(2,len(tempplus[count2].split("`")[0])),tempplus[count2].split("`")[1]))
		# Check for deletion
		if modflag==0:
				print tempminus[count1].split("`")[0].__getslice__(2,len(tempminus[count1].split("`")[0]))+ " has been deleted"
				changes.append(('-',tempminus[count1].split("`")[4],tempminus[count1].split("`")[0].__getslice__(2,len(tempminus[count1].split("`")[0])),tempminus[count1].split("`")[1]))
	# Check for creation
	for count2 in range(len(tempplus)):
		createflag=1
		for count1 in range(len(tempminus)):
			if tempplus[count2].split("`")[4]==tempminus[count1].split("`")[4]:
				createflag=0
		if createflag==1:
			print tempplus[count2].split("`")[0].__getslice__(2,len(tempplus[count2].split("`")[0]))+ " has been created"
			changes.append(('+',tempplus[count2].split("`")[4],tempplus[count2].split("`")[0].__getslice__(2,len(tempplus[count2].split("`")[0])),tempplus[count2].split("`")[1]))
	return changes

def download_files(changes):
	now = datetime.datetime.now()
	for i in changes:
		path=os.getcwd()+path_char+ now.strftime("Evidence-%d-%m-%Y_%H-%M-%S")+path_char
		if i[0]!="-":
			request = service.files().get_media(fileId=i[1])
			if i[3]=="application/vnd.google-apps.folder":
				path+=i[2]
				if not os.path.exists(path):
					print "Downloading folder "+path
					os.makedirs(path)	
					print "Downloaded 100%.\n"
			else:
				path+=i[2].__getslice__(0,len(i[2])-i[2][::-1].index(path_char))
				if not os.path.exists(path):
					os.makedirs(path)
				fh=io.FileIO(path+i[2].__getslice__(len(i[2])-i[2][::-1].index(path_char),len(i[2])), 'wb')
				downloader = MediaIoBaseDownload(fh, request)
				done = False
				while done is False:
					status, done = downloader.next_chunk()
					print "Downloading "+path+i[2].__getslice__(len(i[2])-i[2][::-1].index(path_char),len(i[2]))+"...."
					print "Downloaded %d%%." % int(status.progress() * 100)+"\n"

#Get Authenticated
creds = get_credentials('https://www.googleapis.com/auth/drive') #Full Access 
service = build('drive', version='v3', credentials=creds)




#Start Logging the currentstate
currentstate=open('currentstate.txt','wb')

#Start iterating and listing from the root folder
print "\nCurrent Folder Stucture and Last Modified Time:-\n"
try:
	iter_folder(id=config.get('SETTINGS', 'PARENT_FOLDER_ID'),parent_path=config.get('SETTINGS', 'PARENT_FOLDER_NAME')+path_char,currentstate=currentstate)
except:
	print "\nThe set PARENT_FOLDER_ID in thuppu.config file seems invalid. \n\nFor how to's of  finding folder ID  go to :- \n\"https://googleappsscriptdeveloper.wordpress.com/2017/03/04/how-to-find-your-google-drive-folder-id/\""
	os._exit(1)
currentstate.close()

print "\nChanges from previous state:-\n"

#Checking if thuppu is being run for firsttime
if os.path.exists("laststate.txt"):
	pass
else:
	open("laststate.txt", 'ab').close()
	
changes=finding_diff(previousstate=open("laststate.txt","r").readlines(),currentstate=open("currentstate.txt","r").readlines())

if changes == None:
	print "Nothing to download"
	os.remove("currentstate.txt")
else:
	print "\nDownloading Files:-\n"
	download_files(changes)
	os.remove("laststate.txt")
	os.rename("currentstate.txt","laststate.txt")
