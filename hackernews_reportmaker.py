from bs4 import BeautifulSoup
import urllib2
import re
import html2text
import time
import calendar
import sys

def sublink_finder(url):
	page=urllib2.urlopen(url)
	soup = BeautifulSoup(page.read() ,'html.parser')
	sublinks=soup.find_all('a',{'class' : 'url entry-title page-link'})
	for link in sublinks:
		content_parser(link.attrs['href'])
	next_page=soup.find_all('a' , {'id' :"Blog1_blog-pager-older-link"})[0]
	sublink_finder(next_page.attrs['href'])
	
def content_parser(url):
	if (any(blurl in url for blurl in blacklist_html)):
		pass
	else:
		page=urllib2.urlopen(url)
		soup = BeautifulSoup(page.read() ,'html.parser')
		title=soup.find('a',{'class':'url entry-title page-link'}).text
		date=soup.find('span',{'class':'dtstamp author'}).text.encode('utf-8')
		date=date.__getslice__(25,date.__len__())
		tempdate=date.replace(",","").split()
		datecomp=tempdate[2]+"/"+str(list(calendar.month_name).index(tempdate[1]))+"/"+tempdate[3]
		
		try:
			if time.strptime(sys.argv[1],"%d/%m/%Y") > time.strptime(datecomp,"%d/%m/%Y"):
				exit()
		except :
			print "Usage: python <this_script> <from_date> \n\nPlease note that date should be in dd/mm/yyyy"
			exit()
			
		author=soup.find('span',{'class':'author vcard byline'}).text.strip('\n')
		content=html2text.html2text(str(soup.find('div',{'id':'articlebodyonly'})).decode('utf-8'))
		internal_links=set(re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',content.replace("\n","").replace(")"," ")))
		ref_links=[]
		image_links=[]
		for link in internal_links:
			if link.endswith("png") or link.endswith("jpg") or link.endswith("jpeg") :
				image_links.append(link)
			else:
				if any(blurl in link for blurl in blacklist_urls):
					pass
				else:
					ref_links.append(link)
					
		# #For CSV or SQLITE (Will be implemented if needed in future)
		# print "Title:"+title.encode('utf-8')
		# print "Link:" + url
		# print "Date:" + date
		# print "Author:"+author
		# #print "Body:\n"+content.encode('utf-8')
		# print "Reference Links:"+str(ref_links)
		# print "Image Links:"+str(image_links)
		# print "-"*50
		global count
		count+=1
		#For HTML Report 
		html_title=str(soup.find('h1',{'class':'post-title url'})).replace("rel=\"bookmark\">","rel=\"bookmark\">"+str(count)+". ")
		html_dateauthor=soup.find('div',{'class':'postmeta'})
		html_articlebody=soup.find('div',{'id':'articlebodyonly'})
		
		print html_title
		print html_dateauthor
		print html_articlebody
		
		print "="*201
		

blacklist_urls=["bp.blogspot.com","thehackernews.com"]
blacklist_html=["ethical-hacking-online-training.html","online-cissp-certification-training.html","cyber-security-certification-training.html","hacker-news-cybersecurity.html"]
count =0
sublink_finder("http://thehackernews.com")