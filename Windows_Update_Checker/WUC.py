
from scrapy import Selector
from tqdm import tqdm
import requests
import math
import re
import sqlite3
import subprocess
import sys,os
import tempfile
import xml.etree.ElementTree as ET
import time
from fuzzywuzzy import fuzz


#Global Variables

conn = sqlite3.connect('MSPatch.db')
c=conn.cursor()
cabname=[]
extractedcabs=[]
rangestart=[]
updatetempfiles_path= tempfile.gettempdir()+"\\winupdate"
errorlog=open("errorlog.txt","w")
host_name=""
os_name=""
os_version=""
arch=""
language=""
patches=[]
programs=[]
final_updates_list=[]
solved_revisionids=[]
blacklisted=["Microsoft","MUI","Pro","(English)","Components","32-bit","64-bit"]

#Helper Functions

def remove_blacklisted_strings(buff):
	for i in blacklisted:
		if i in buff:
			buff=buff.replace(i,"")
	return buff

def concatenate_list_data(list):
    result= ''
    for element in list:
        result += str(element)
    return result

def parse_wssuscn2cab(buff):
	global cabname,rangestart,extractedcabs,errorlog
	scrape=Selector(text=buff)
	updateid=scrape.xpath("//update/@updateid").extract_first()
	
	if c.execute("select updateid from MSPatchTable where updateid=\""+updateid+"\"").fetchall().__len__()>0:
		return
	creationdate=scrape.xpath("//update/@creationdate").extract_first()
	revisionid=scrape.xpath("//update/@revisionid").extract_first()
	cabtoextract=""
	for i in range(cabname.__len__()-1):

		if int(revisionid)>int(rangestart[i]):
			pass
		else:
			cabtoextract=cabname[i]
			break
	if cabtoextract=="":
		cabtoextract=cabname[cabname.__len__()-1]
	
	if cabtoextract in extractedcabs:
		pass
	else:
		for f in os.listdir(updatetempfiles_path):
			if os.path.isdir(updatetempfiles_path+"\\"+f):
				os.system("rmdir "+updatetempfiles_path+"\\"+f+" /S /Q")
		mute=subprocess.check_output(".\\7z.exe x "+updatetempfiles_path+"\\wsusscn2.cab "+cabtoextract+" -o"+updatetempfiles_path+" -y")
		mute=subprocess.check_output(".\\7z.exe x "+updatetempfiles_path+"\\"+cabtoextract+" -o"+updatetempfiles_path+" -y")
		os.system("del "+updatetempfiles_path+"\\"+cabtoextract)
		extractedcabs.append(cabtoextract)
	
	prerequisite=list_to_string(scrape.xpath("//prerequisites/*/@id").extract())
	supersededby=list_to_string(scrape.xpath("//supersededby/*/@id").extract())
	if  scrape.xpath("//category[@type = 'Company']/@id").extract_first():
		Category_Company =  list_to_string(scrape.xpath("//category[@type = 'Company']/@id").extract_first())
		Category_Product= list_to_string(scrape.xpath("//category[@type = 'Product']/@id").extract())
		Category_ProductFamily=list_to_string(scrape.xpath("//category[@type = 'ProductFamily']/@id").extract())
		Category_UpdateClassification=list_to_string(scrape.xpath("//category[@type = 'UpdateClassification']/@id").extract())
		
		
	else:
		Category_Company=Category_Product=Category_ProductFamily=Category_UpdateClassification=prerequisites=""

	try:
		scrape=Selector(text=(re.sub(r'[^\x00-\x7f]','',concatenate_list_data(open(updatetempfiles_path+"\\c\\"+revisionid,"r").readlines()).replace("\n","").replace("\r","").replace("\t","").strip(" "))))
		supersedes=list_to_string(scrape.xpath("//supersededupdates/updateidentity/@updateid").extract())
	except Exception as e:
		errorlog.write(updateid+":"+revisionid+": "+str(e)+" \n")
		supersedes=""
	
	try:
		scrape=Selector(text=(re.sub(r'[^\x00-\x7f]','',concatenate_list_data(open(updatetempfiles_path+"\\l\\en\\"+revisionid,"r").readlines()).replace("\n","").replace("\r","").replace("\t","").strip(" "))))
		title=re.sub(r'[^\x00-\x7f]','',str(scrape.xpath("//title/text()").extract_first()))
		description=re.sub(r'[^\x00-\x7f]','',str(scrape.xpath("//description/text()").extract_first()))
	except Exception as e:
		errorlog.write(updateid+":"+revisionid+": "+cabtoextract+":"+str(e)+" \n")
		title=""
		description=""
	try:
		scrape=Selector(text=(re.sub(r'[^\x00-\x7f]','',concatenate_list_data(open(updatetempfiles_path+"\\s\\"+revisionid,"r").readlines()).replace("\n","").replace("\r","").replace("\t","").strip(" "))))
		msrcseverity=str(scrape.xpath("//properties/@msrcseverity").extract_first())
		msrcnumber=str(scrape.xpath("//securitybulletinid/text()").extract_first())
		kb="KB"+str(scrape.xpath("//properties/kbarticleid/text()").extract_first())
		languages=list_to_string(scrape.xpath("//properties/language/text()").extract())
		
	except Exception as e:
		errorlog.write(updateid+":"+revisionid+": "+cabtoextract+":"+str(e)+" \n")
		msrcnumber=""
		msrcseverity=""
		kb=""
		languages=""
		
	try:
		scrape=Selector(text=(re.sub(r'[^\x00-\x7f]','',concatenate_list_data(open(updatetempfiles_path+"\\x\\"+revisionid,"r").readlines()).replace("\n","").replace("\r","").replace("\t","").strip(" "))))
		category=str(scrape.xpath("//categoryinformation/@categorytype").get())
	except Exception as e:
		errorlog.write(updateid+":"+revisionid+": "+cabtoextract+":"+str(e)+" \n")
		category=""
	
	try:	
		params=(updateid,revisionid,creationdate,Category_Company,Category_Product,Category_ProductFamily,Category_UpdateClassification,prerequisite,title,description,msrcseverity,msrcnumber,kb,languages,category,supersededby,supersedes)
		c.execute('Insert into MSPatchTable values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',params) 
	except Exception as e:
		errorlog.write(updateid+":"+revisionid+": "+str(e)+" \n")
		pass
	
def download_cab():
	print "\n\nThis is going to take some time. Please be patient .... \n\nGrabbing a cup of coffee might be a good idea right now !! :P \n\nStep 1 out of 3 :- Downloading Official WSUS Update Cab File\n\n"
	url="http://go.microsoft.com/fwlink/?linkid=74689"
	r=requests.get(url, stream=True)
	total_size = int(r.headers.get('content-length', 0)); 
	block_size = 1024
	wrote = 0 
	if os.path.isdir(updatetempfiles_path):
		pass
	else:
		mute=subprocess.check_output("mkdir "+updatetempfiles_path)
		
	with open(updatetempfiles_path+'\\wsusscn2.cab', 'wb') as f:
		for data in tqdm(r.iter_content(block_size), total=math.ceil(total_size//block_size) , unit='KB', unit_scale=True):
			wrote = wrote  + len(data)
			f.write(data)
	if total_size != 0 and wrote != total_size:
		print("ERROR, something went wrong")
		sys.exit()

def list_to_string(buff):
	return str(buff).replace("u'","").replace("[","").replace("]","").replace("'","").replace("\r","").replace("\n","")

def parse_sysinfo(sysinfo_file):
	global host_name,os_name,os_version,arch,language,patches
	hotfix_parsed=0
	count=0
	with open(sysinfo_file,"r") as inputfile:
		for line in inputfile:
			line_c=line.replace("\x00","")
			if 'Host Name:' in line_c and hotfix_parsed==0:
				host_name=line_c.split(":")[1].strip(" ").strip("\n").strip("\r")
			elif 'OS Name:' in line_c and hotfix_parsed==0:
				os_name=line_c.split(":")[1].strip(" ").strip("\n").strip("\r")
			elif line_c.startswith('OS Version:') and hotfix_parsed==0:
				os_version=line_c.split(":")[1].strip(" ").strip("\n").strip("\r")
			elif 'System Type:' in line_c and hotfix_parsed==0:
				arch=line_c.split(":")[1].strip(" ").strip("\n").strip("\r")
			elif 'System Locale:' in line_c and hotfix_parsed==0:
				language=line_c.split(":")[1].strip(" ").strip("\n").strip("\r")
			elif  'Hotfix(s):' in line_c or hotfix_parsed>0 :
				if hotfix_parsed>0 and hotfix_parsed<=count:
					patches.append(line_c.strip(" ").split(":")[1].strip("\r\n").strip(" "))
					hotfix_parsed+=1
				elif hotfix_parsed ==0:
						count=line_c.split(":")[1].strip(" ").split(" ")[0]
						if "N/A" in count:
							count=0
						else:
							count=int(line_c.split(":")[1].strip(" ").split(" ")[0])
							hotfix_parsed=1
					
				else:
					break		

def parse_programslist(programs_file):
	global programs
	#command wmic product get name,version,vendor,installdate
	with open(programs_file,"r") as inputfile:
		for line in inputfile:
			line_c=line.replace("\x00","")
			if "Microsoft Corporation" in line_c:
				programs.append(line_c.__getslice__(8,line_c.index("Microsoft Corporation")).strip(" "))
	
def solve_supersede_updateids(applicable_updates):
	global final_updates_list
	superseded_updates=[]
	applicable_updates_query=str(applicable_updates).replace("u'","'").replace("[","(").replace("]",")")
	record=c.execute("select supersededby from MSPatchTable where updateid in "+applicable_updates_query+";")
	for i,j in zip(record.fetchall(),range(0,applicable_updates.__len__())):
		if i[0].__len__()==0:
			final_updates_list.append(applicable_updates[j])
			record=c.execute("select revisionid from MSPatchTable where updateid ='"+applicable_updates[j]+"';")
			solved_revisionids.append(record.fetchall()[0][0])
		else:
			solve_supersede_revisionids(i[0])
	print final_updates_list
	
def solve_supersede_revisionids(revisionids):
	for i in revisionids.split(","):
		if i.strip(" ") in solved_revisionids:
			continue
		record=c.execute("select updateid,supersededby from MSPatchTable where revisionid='"+i.strip(" ")+"' ;")
		for j in record.fetchall():
			if j[1].__len__()==0:
				if j[0] in final_updates_list:
					continue
				else:
					final_updates_list.append(j[0])
					solved_revisionids.append(i.strip(" "))
			else:
				solve_supersede_revisionids(j[1])
				solved_revisionids.append(i.strip(" "))

				
#Main Functions
			
def Update():
	global cabname,rangestart,i,errorlog
	#download_cab()
	print "\n\nStep 2 out of 3 :- Reading data from cab file and feeding the database\n\n"
	mute=subprocess.check_output(".\\7z.exe x "+updatetempfiles_path+"\\wsusscn2.cab index.xml -o"+updatetempfiles_path+" -y")
	mute=subprocess.check_output(".\\7z.exe x "+updatetempfiles_path+"\\wsusscn2.cab package.cab -o"+updatetempfiles_path+" -y")
	mute=subprocess.check_output(".\\7z.exe x "+updatetempfiles_path+"\\package.cab package.xml -o"+updatetempfiles_path+" -y")
	os.system("del \""+updatetempfiles_path+"\\package.cab\"")
	indexfile=open(updatetempfiles_path+"\\index.xml","r")
	indexf=indexfile.readlines()[0]
	scrape=Selector(text=indexf)
	cabname=scrape.xpath("//cab/@name").extract()
	rangestart=scrape.xpath("//cab/@rangestart").extract()
	indexfile.close()
	
	context = ET.iterparse(updatetempfiles_path+'\\package.xml', events=('end',))
	
	#Counting the number of tags to process for our status bar for Step 2
	i=0
	for event,elem in context:
		i+=1
	
	context = ET.iterparse(updatetempfiles_path+'\\package.xml', events=('end',))
	for event, elem in tqdm(context,total=i):
		if elem.tag == '{http://schemas.microsoft.com/msus/2004/02/OfflineSync}Update':
			parse_wssuscn2cab(ET.tostring(elem).replace("ns0:",""))
	print "\n\nStep 3 out of 3 :- Clearing temp cache \n\n"
	os.system("rmdir "+updatetempfiles_path+" /s /Q")
	print "Update Complete .....!! :) "
	conn.commit()
	errorlog.close()	

def scan_sysinfo(sysinfo_file):
	global os_name,language,arch,patches
	
	
	parse_sysinfo(sysinfo_file)
	si_applicable_updates=[]
	si_os_updateid=""
	si_lang=language.split(";")[0]
	si_arch_updateid=""
	best_match_length=0
	si_unwanted_products=""
	
	record=c.execute("select updateid,title from MSPatchTable where category='Product' and title not like '%Drivers%';")
	for t in record.fetchall():
		if t[1] in os_name and t[1].__len__()>best_match_length:
			si_os_updateid=t[0]
			best_match_length=t[1].__len__()
	best_match_length=0
	
	if si_os_updateid=="":
		print "The information regarding this product currently does not exist in the database. Try updating !!"
		return
	if arch=="x64-based PC":
		si_arch_updateid=c.execute("select updateid from MSPatchTable where title='AMD64' and category='Arch';").fetchall()[0][0]
	elif arch=="x86-based PC":
		si_arch_updateid=c.execute("select updateid from MSPatchTable where title='X86' and category='Arch';").fetchall()[0][0]
	elif arch.__contains__("ARM"):
		if arch.__contains__("64"):
			si_arch_updateid=c.execute("select updateid from MSPatchTable where title='ARM64'and category='Arch';").fetchall()
		else:
			si_arch_updateid=c.execute("select updateid from MSPatchTable where title='ARM' and category='Arch';").fetchall()[0][0]
	elif arch.__contains__("Itanium"):
		si_arch_updateid=c.execute("select updateid from MSPatchTable where title='IA64' and category='Arch';").fetchall()[0][0]
	
	#To find product ids that belog to other microsoft products, this is to ensure that we remove all these from our search and get only pure os and arch based applicable updates
	#(Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion").ReleaseId for getting release id  or reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v ReleaseId
	
	si_unwanted_products=""
	record=c.execute("Select updateid from MSPatchTable where category='Product' and updateid!='"+si_os_updateid+"';")
	
	#To filter only OS specific updates
	for t in record.fetchall():
		si_unwanted_products+="and prerequisite not like '%"+t[0]+"%' "
	#Specific queryfor ARM64 based clients because MS has two updateids for ARM64 , God knows why !!
	if arch.__contains__("ARM") and arch.__contains__("64"):
		record=c.execute("select updateid,title,languages from MSPatchTable where prerequisite like '%"+si_os_updateid+"%' and (prerequisite like '%"+si_arch_updateid[0][0]+"%' or prerequisite like '%"+si_arch_updateid[1][0]+"%') and ((languages in ('','None')) or (languages like '%"+si_lang+"%')) "+si_unwanted_products+" and updateclassification='0fa1201d-4330-4fa8-8ae9-b877473b6441';")
	else:
		record=c.execute("select updateid,title,languages from MSPatchTable where prerequisite like '%"+si_os_updateid+"%' and prerequisite like '%"+si_arch_updateid+"%' and ((languages in ('','None')) or (languages like '%"+si_lang+"%')) "+si_unwanted_products+" and updateclassification='0fa1201d-4330-4fa8-8ae9-b877473b6441';")
	
	version="1709"
	for t in record.fetchall():
		if t[1].__contains__("Version"):
			if t[1].__contains__(version):
				si_applicable_updates.append(t[0])
		else:
			si_applicable_updates.append(t[0])
			
	solve_supersede_updateids(si_applicable_updates)

def scan_programlist(programs_file):
	parse_programslist(programs_file)
	pl_program_updateid=[]
	temp=""
	best_match_length=0
	records=c.execute("select updateid,title from MSPatchTable where category='Product' and title not like '%Drivers%';").fetchall()
	for i in programs:
		ratio=0
		fuzzratio=0
		tempprogramname=""
		temprecordname=""
		for t in records:
			fuzzratio=fuzz.QRatio(remove_blacklisted_strings(re.sub(r'[^\x00-\x7f]','',t[1])),remove_blacklisted_strings(re.sub(r'[^\x00-\x7f]','',i)))
			if fuzzratio > ratio:
				tempprogramname=i
				temprecordname=t[1]
				ratio=fuzzratio
		print temprecordname+" : "+tempprogramname+" : "+str(ratio)
	
	
	
			
Update()