# Dirty-Scripts

Objective of this repo is to save my dirty scripts that helps me on some repeated tasks. This repo acts as a backup for my scripts.


PS: All the scripts here are written just to get the work done. Hence expect some nasty coding and trash in this. :P This repo will be updated with new scripts as and when I come across any repeated tasks and write a script to automate it.

1. hackernews_reportmaker - Helps in making a consolidated report consisting of all the news feeds present in thehackernews.com site from the day of running the script to the date (back date)  provided as an argument. Helps me in gathering security news for making news bytes presentations for various periodic local security meetups.

2. timezone.py - Helps me during forensic analysis for correlation of times from evidences from various timezones. The script gives out a table consisting of corresponding times across various timezones for a given time and the concerned timezone. Data of timezone conversion was collected from the site: https://www.epochconverter.com/timezones.

3. Windows_Update_Checker - This tool was initially build to audit a system for exisitence of available patches. The major objective was to build a tool to check a given windows system's update status passively in an offline environment using the output of command such as systeminfo.exe , wmic qfe list, wmic product get name etc ... The tool downloads official WSUS cab file from the official Microsoft Site and feeds the details into a local SQLite database. The tool is executed with arguments as output from the mentioned caommands. Tool analyses the os version, language, architecture, programs etc and checks the database and gives out the list of patches to be applied to the system. 

The result may not be accurate as the patches are checked with string names wheras original WSUS tool runs set of checks on a system actively to identify the applicable patches. This tool can be used just to get an understanding of the patching maturity in the system.
This project has been temporarily kept on hold to search on how to proceed with product name comparison between the installed product name in the system and one officially provided by Microsoft. The fuzzy comparison was initially utilised to check for nearest name possible but however a concrete threshold could not be determined to give nearest matching product. This is to check for patches in the database for products installed. Challenge can be understood by the following example:-

Installed Product Name: Microsoft Visual C++ 2015 x86 Additional Runtime - 14.0.23506 (No Official Product Name for this product as part of WSUS cab package)
Closest Product Name in the database : Microsoft Visual Studio
But fuzzy ratios are between 40-50 for the above comparision which is not a good ratio as the same ratio gives rise to false positives. 

Please feel free to use the script and test and do let me know if you find it useful and if you have found working logic for the above challenge. My E-mail Id is godzillagenx@gmail.com.
