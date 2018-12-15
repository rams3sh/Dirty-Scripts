import sys
import os 

def usage():
	print "\nUsage:-\npython kaima-thuppu.py < to be converted to which supported os ? > <laststate.txt file path>"
	
	print "Supported OS :- windows,mac,linux"
	print "\nExample usage:- \nTo convert a windows laststate file to mac laststate file\npython kaima-thuppu.py mac laststate.txt"

try:
	filein=open(sys.argv[2],"r")
	fileout=open("laststate_"+sys.argv[1]+".txt","wb")

	if sys.argv[1]=="windows":
		for i in filein.readlines():
			line=i.split("`")
			for j in range(len(line)):
				if j==0:
					fileout.write(line[0].replace("/","\\"))
				else:
					fileout.write("`"+line[j])
		print "Converted Successfully !!\nRename laststate_windows.txt to laststate.txt before using with thuppu."
	elif sys.argv[1]=="linux" or sys.argv[1]=="mac":
		for i in filein.readlines():
			line=i.split("`")
			for j in range(len(line)):
				if j==0:
					fileout.write(line[0].replace("\\","/"))
				else:
					fileout.write("`"+line[j])
		print "Converted Successfully !!\nRename laststate_linux.txt to laststate.txt before using with thuppu."
	else:
		print "Given OS not supported"
		usage()
except:
	usage()
	print "Check if your OS and file path of the laststate.txt is correct"
