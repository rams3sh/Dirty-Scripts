# Dirty-Scripts

Objective of this repo is to save my dirty scripts that helps me on some repeated tasks. This repo acts as a backup for my scripts.


PS: All the scripts here are written just to get the work done. Hence expect some nasty coding and trash in this. :P This repo will be updated with new scripts as and when I come across any repeated tasks and write a script to automate it.

1. hackernews_reportmaker - Helps in making a consolidated report consisting of all the news feeds present in thehackernews.com site from the day of running the script to the date (back date)  provided as an argument. Helps me in gathering security news for making news bytes presentations for various periodic local security meetups.

2. timezone.py - Helps me during forensic analysis for correlation of times from evidences from various timezones. The script gives out a table consisting of corresponding times across various timezones for a given time and the concerned timezone. Data of timezone conversion was collected from the site: https://www.epochconverter.com/timezones.

3. Thupparivalan - Tamil world which means to Investigator/Detective.The script was used to detect changes in a given folder within a google drive. Helps me to analyze whenever a file is uploaded / deleted / modified within the scope of a give parent folder which needs to be monitored.Refer the Readme of the folder for more details.

4. AWSome_reporter - This tool helps in converting json output received from queried through AWS developer API to an equivalent sqlite3 db and an excel file. It uses flatten_json library to flatten the multi level json. It replicates all the values of a given level for x times where x is the maximum values accomodated in a given level for making a meaningful record. The script is very inefficient from optimization perspective as any other script in this repo but gets the job done. Have release an exe version of it as part of releases for win 64 guys.  Huge shout out to flatten_json (https://pypi.org/project/flatten_json/) which is the soul of this tool.Check it out.
    
    
