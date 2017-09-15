from datetime import datetime , timedelta
from sys import argv

timezone=[["Atlantic/Azores (AZOST)","AZOST","GMT +00:00",0],
["America/Scoresbysund (EGST)","EGST","GMT +00:00",0],
["Africa/Abidjan (GMT)","GMT","GMT +00:00",0],
["UTC (UTC)","UTC","GMT +00:00",0],
["Europe/Guernsey (BST)","BST1","GMT +01:00",3600],
["Africa/Algiers (CET)","CET","GMT +01:00",3600],
["Europe/Dublin (IST)","IST2","GMT +01:00",3600],
["Africa/Bangui (WAT)","WAT","GMT +01:00",3600],
["Africa/Casablanca (WEST)","WEST","GMT +01:00",3600],
["Antarctica/Troll (+02)","+2","GMT +02:00",7200],
["Africa/Blantyre (CAT)","CAT","GMT +02:00",7200],
["Africa/Ceuta (CEST)","CEST","GMT +02:00",7200],
["Africa/Cairo (EET)","EET","GMT +02:00",7200],
["Africa/Johannesburg (SAST)","SAST","GMT +02:00",7200],
["Africa/Windhoek (WAST)","WAST","GMT +02:00",7200],
["Antarctica/Syowa (+03)","+3","GMT +03:00",10800],
["Asia/Aden (AST)","AST2","GMT +03:00",10800],
["Africa/Addis Ababa (EAT)","EAT","GMT +03:00",10800],
["Asia/Amman (EEST)","EEST","GMT +03:00",10800],
["Asia/Jerusalem (IDT)","IDT","GMT +03:00",10800],
["Europe/Moscow (MSK)","MSK","GMT +03:00",10800],
["Asia/Baku (+04)","+4","GMT +04:00",14400],
["Asia/Dubai (GST)","GST1","GMT +04:00",14400],
["Indian/Mauritius (MUT)","MUT","GMT +04:00",14400],
["Indian/Reunion (RET)","RET","GMT +04:00",14400],
["Indian/Mahe (SCT)","SCT","GMT +04:00",14400],
["Asia/Kabul (AFT)","AFT","GMT +04:30",16200],
["Asia/Tehran (IRDT)","IRDT","GMT +04:30",16200],
["Antarctica/Mawson (+05)","+5","GMT +05:00",18000],
["Indian/Maldives (MVT)","MVT","GMT +05:00",18000],
["Asia/Karachi (PKT)","PKT","GMT +05:00",18000],
["Asia/Colombo (+0530)","+05:30","GMT +05:30",19800],
["Asia/Kolkata (IST)","IST1","GMT +05:30",19800],
["Asia/Kathmandu (NPT)","NPT","GMT +05:45",20700],
["Antarctica/Vostok (+06)","+6","GMT +06:00",21600],
["Asia/Dhaka (BDT)","BDT","GMT +06:00",21600],
["Asia/Thimphu (BTT)","BTT","GMT +06:00",21600],
["Indian/Chagos (IOT)","IOT","GMT +06:00",21600],
["Asia/Urumqi (XJT)","XJT","GMT +06:00",21600],
["Indian/Cocos (CCT)","CCT","GMT +06:30",23400],
["Asia/Yangon (MMT)","MMT","GMT +06:30",23400],
["Antarctica/Davis (+07)","+7","GMT +07:00",25200],
["Indian/Christmas (CXT)","CXT","GMT +07:00",25200],
["Asia/Bangkok (ICT)","ICT","GMT +07:00",25200],
["Asia/Jakarta (WIB)","WIB","GMT +07:00",25200],
["Asia/Irkutsk (+08)","+8","GMT +08:00",28800],
["Australia/Perth (AWST)","AWST","GMT +08:00",28800],
["Asia/Brunei (BNT)","BNT","GMT +08:00",28800],
["Asia/Macau (CST)","CST2","GMT +08:00",28800],
["Asia/Hong Kong (HKT)","HKT","GMT +08:00",28800],
["Asia/Hovd (HOVST)","HOVST","GMT +08:00",28800],
["Asia/Kuala Lumpur (MYT)","MYT","GMT +08:00",28800],
["Asia/Manila (PHT)","PHT","GMT +08:00",28800],
["Asia/Singapore (SGT)","SGT","GMT +08:00",28800],
["Asia/Makassar (WITA)","WITA","GMT +08:00",28800],
["Asia/Pyongyang (KST)","KST1","GMT +08:30",30600],
["Australia/Eucla (ACWST)","ACWST","GMT +08:45",31500],
["Asia/Chita (+09)","+9","GMT +09:00",32400],
["Asia/Choibalsan (CHOST)","CHOST","GMT +09:00",32400],
["Asia/Tokyo (JST)","JST","GMT +09:00",32400],
["Asia/Seoul (KST)","KST2","GMT +09:00",32400],
["Pacific/Palau (PWT)","PWT","GMT +09:00",32400],
["Asia/Dili (TLT)","TLT","GMT +09:00",32400],
["Asia/Ulaanbaatar (ULAST)","ULAST","GMT +09:00",32400],
["Asia/Jayapura (WIT)","WIT","GMT +09:00",32400],
["Australia/Adelaide (ACST)","ACST","GMT +09:30",34200],
["Antarctica/DumontDUrville (+10)","+10","GMT +10:00",36000],
["Australia/Brisbane (AEST)","AEST","GMT +10:00",36000],
["Pacific/Guam (ChST)","ChST","GMT +10:00",36000],
["Pacific/Chuuk (CHUT)","CHUT","GMT +10:00",36000],
["Pacific/Port Moresby (PGT)","PGT","GMT +10:00",36000],
["Australia/Lord Howe (LHST)","LHST","GMT +10:30",37800],
["Antarctica/Casey (+11)","+11","GMT +11:00",39600],
["Pacific/Bougainville (BST)","BST2","GMT +11:00",39600],
["Pacific/Kosrae (KOST)","KOST","GMT +11:00",39600],
["Antarctica/Macquarie (MIST)","MIST","GMT +11:00",39600],
["Pacific/Noumea (NCT)","NCT","GMT +11:00",39600],
["Pacific/Norfolk (NFT)","NFT","GMT +11:00",39600],
["Pacific/Pohnpei (PONT)","PONT","GMT +11:00",39600],
["Pacific/Guadalcanal (SBT)","SBT","GMT +11:00",39600],
["Pacific/Efate (VUT)","VUT","GMT +11:00",39600],
["Asia/Anadyr (+12)","+12","GMT +12:00",43200],
["Pacific/Fiji (FJT)","FJT","GMT +12:00",43200],
["Pacific/Tarawa (GILT)","GILT","GMT +12:00",43200],
["Pacific/Kwajalein (MHT)","MHT","GMT +12:00",43200],
["Pacific/Nauru (NRT)","NRT","GMT +12:00",43200],
["Antarctica/McMurdo (NZST)","NZST","GMT +12:00",43200],
["Pacific/Funafuti (TVT)","TVT","GMT +12:00",43200],
["Pacific/Wake (WAKT)","WAKT","GMT +12:00",43200],
["Pacific/Wallis (WFT)","WFT","GMT +12:00",43200],
["Pacific/Chatham (CHAST)","CHAST","GMT +12:45",45900],
["Pacific/Tongatapu (+13)","+13","GMT +13:00",46800],
["Pacific/Enderbury (PHOT)","PHOT","GMT +13:00",46800],
["Pacific/Fakaofo (TKT)","TKT","GMT +13:00",46800],
["Pacific/Apia (WSST)","WSST","GMT +13:00",46800],
["Pacific/Kiritimati (LINT)","LINT","GMT +14:00",50400],
["Atlantic/Cape Verde (CVT)","CVT","GMT -01:00",-3600],
["America/Noronha (FNT)","FNT","GMT -02:00",-7200],
["Atlantic/South Georgia (GST)","GST2","GMT -02:00",-7200],
["America/Miquelon (PMDT)","PMDT","GMT -02:00",-7200],
["America/Godthab (WGST)","WGST","GMT -02:00",-7200],
["America/St Johns (NDT)","NDT","GMT -02:30",-9000],
["Antarctica/Rothera (-03)","-3","GMT -03:00",-10800],
["America/Glace Bay (ADT)","ADT","GMT -03:00",-10800],
["America/Argentina/Buenos Aires (ART)","ART","GMT -03:00",-10800],
["America/Araguaina (BRT)","BRT","GMT -03:00",-10800],
["America/Santiago (CLST)","CLST","GMT -03:00",-10800],
["Atlantic/Stanley (FKST)","FKST","GMT -03:00",-10800],
["America/Cayenne (GFT)","GFT","GMT -03:00",-10800],
["America/Paramaribo (SRT)","SRT","GMT -03:00",-10800],
["America/Montevideo (UYT)","UYT","GMT -03:00",-10800],
["America/Boa Vista (AMT)","AMT","GMT -04:00",-14400],
["America/Anguilla (AST)","AST1","GMT -04:00",-14400],
["America/La Paz (BOT)","BOT","GMT -04:00",-14400],
["America/Havana (CDT)","CDT2","GMT -04:00",-14400],
["America/Detroit (EDT)","EDT","GMT -04:00",-14400],
["America/Guyana (GYT)","GYT","GMT -04:00",-14400],
["America/Asuncion (PYT)","PYT","GMT -04:00",-14400],
["America/Caracas (VET)","VET","GMT -04:00",-14400],
["America/Eirunepe (ACT)","ACT","GMT -05:00",-18000],
["America/Bahia Banderas (CDT)","CDT1","GMT -05:00",-18000],
["America/Bogota (COT)","COT","GMT -05:00",-18000],
["Pacific/Easter (EASST)","EASST","GMT -05:00",-18000],
["America/Guayaquil (ECT)","ECT","GMT -05:00",-18000],
["America/Atikokan (EST)","EST","GMT -05:00",-18000],
["America/Lima (PET)","PET","GMT -05:00",-18000],
["America/Belize (CST)","CST1","GMT -06:00",-21600],
["Pacific/Galapagos (GALT)","GALT","GMT -06:00",-21600],
["America/Boise (MDT)","MDT","GMT -06:00",-21600],
["America/Creston (MST)","MST","GMT -07:00",-25200],
["America/Dawson (PDT)","PDT","GMT -07:00",-25200],
["America/Anchorage (AKDT)","AKDT","GMT -08:00",-28800],
["Pacific/Pitcairn (PST)","PST","GMT -08:00",-28800],
["Pacific/Gambier (GAMT)","GAMT","GMT -09:00",-32400],
["America/Adak (HDT)","HDT","GMT -09:00",-32400],
["Pacific/Marquesas (MART)","MART","GMT -09:30",-34200],
["Pacific/Rarotonga (CKT)","CKT","GMT -10:00",-36000],
["Pacific/Honolulu (HST)","HST","GMT -10:00",-36000],
["Pacific/Tahiti (TAHT)","TAHT","GMT -10:00",-36000],
["Pacific/Niue (NUT)","NUT","GMT -11:00",-39600],
["Pacific/Midway (SST)","SST","GMT -11:00",-39600]]

try:
	input1=argv[1]
	d=datetime.strptime(input1, "%d-%m-%Y-%H:%M:%S")
	input2=argv[2]
	if input2== "AST" or input2=="BST" or input2=="CDT" or input2=="CST" or input2=="GST" or input2=="IST" or input2=="KST":
		print "\nERROR: The given timezone has more than one reference. Please give the appropriate timezone abbreviation as given below. \n"
		for i in range(timezone.__len__()):
			if timezone[i][1].startswith(input2):
				print timezone[i][0]+" ,"+timezone[i][2]+" - "+timezone[i][1]
	else:
		is_Present=False
		GMT=""
		for i in range(timezone.__len__()):
			if timezone[i][1] == input2:
				is_Present=True
				GMT=d-timedelta(seconds=timezone[i][3])
		if GMT < datetime.strptime("1-1-1900-11:00:00","%d-%m-%Y-%H:%M:%S"):
			print "\nERROR: The given arguments are invalid. \nUsage:- timezone <DD-MM-YYYY-hh:mm:ss> <Timezone-Abbreviation> where Date Time > 1-1-1900 11:00:00 GMT"
		
		if is_Present:
			print "\nTime: "+str(input1)+" "+str(input2)
			print "\nThe corresponding time across the globe below:-\n"
			print " "+"-"*89
			print " |S.NO"+" | "+"Timezone"+" "*(36-"Timezone".__len__())+" "*(7-"GMT".__len__())+" | "+"GMT"+" "*7+" | "+"Time (dd-mm-yy hh:mm:ss)"+"|"
			print " |"+"-"*5+"|"+"-"*42+"|"+"-"*12+"|"+"-"*25+"|"
			for i in range(timezone.__len__()):
				t=(GMT+timedelta(seconds=timezone[i][3])).strftime("%d-%m-%y %H:%M:%S")
				print " |"+str(i+1)+" "*(4-str(i+1).__len__())+" | "+timezone[i][0]+" "*(40-str(timezone[i][0]).__len__())+" "*(7-str(timezone[i][2]).__len__())+" | "+timezone[i][2]+" | "+t+" "*7+"|"
			print " "+"-"*89
			print """\nNOTE:\nTo convert from normal/standard time to daylight saving time add 1 hour ( or +3600 seconds ).\nFor example: Eastern Standard Time = GMT-5, add 1 hour: Eastern Daylight Time = GMT-4	"""
		else:
			print "\nERROR: The given arguments are invalid. \nUsage:- timezone <DD-MM-YYYY-hh:mm:ss> <Timezone-Abbreviation> where Date Time > 1-1-1900 11:00:00 GMT"
except:
	print "\nERROR: The given arguments are invalid. \nUsage:- timezone <DD-MM-YYYY-hh:mm:ss> <Timezone-Abbreviation> where Date Time > 1-1-1900-11:00:00 GMT "