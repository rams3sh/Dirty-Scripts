Thupparivalan (Thuppu - Shortform)
----------------------------------

Thupparivalan in tamil means "Detective". It literally translates to "Evidence Analyzer".

The script was written mainly for a daily task where I would have to take the diff of the changed files or folders within a specific parent folder in google drive and analyze for the content. 

This script identifies the changed files alone (created or modified and not deleted items) and downloads to a folder with <DD-MM-YYYY_HH-MM-SS> naming convention within the same folder as Thupparivalan. This was needed as it was a big headache to identify the changed files/ folders manually and download one by one.


Setting up Thuppu :-
-----------------------------------

Pre-Requisites:-
i. Install Python 2.7

ii. Libraries :
  google_api_python_client==1.7.6
  
  Run "pip install google_api_python_client==1.7.6" for installing the library.
  
iii. Download Dirty-Scripts/Thupparivalan folder or download the tool from releases.


Running Thuppu :-
------------------

The tool requires the following files to be in the same folder during the first run:-

i. thupparivalan.py / thupparivalan.exe - The main script / binary

ii. thuppu.config - The config file for the tool

iii. credentials.json - File containing your credentials required to query,fetch and download files using google drive api 

For iii. above, follow the below steps 

Step 1: Go to https://developers.google.com/drive/api/v3/quickstart/python

Step 2: Follow till all steps within  "Step 1: Turn on the Drive API".

Step 3: Copy the downloaded credentials.json in the same folder as thupparivalan and run !!


Set the PARENT_FOLDER_NAME and PARENT_FOLDER_ID in the thuppu.config file.
For how to's of  finding folder ID  go to :-
"https://googleappsscriptdeveloper.wordpress.com/2017/03/04/how-to-find-your-google-drive-folder-id/"

Post all the steps above, you would be required to create token.json file which will have the authorizing details for thuppu to use google drive api using your credentials. Need not bother about it, if this file is not in path , thuppu will automatically guide you in creating one. Create a random project name when requested in the portal.This project name is not significant from usage of this tool.

Refer :https://developers.google.com/drive/api/v3/about-auth for more details about the token. Please note by default the scope of the token is "https://www.googleapis.com/auth/drive" which is equivalent of Full access to your drive. I have used this scope to avoid any permission related errors.


Finally you will have 4 files in your folder :-

i. thupparivalan.py / thupparivalan.exe 

ii. thuppu.config - The config file for the tool with all the parameters set.

iii. credentials.json - File containing your credentials for authenticating into drive api. Not required anymore as it is required intially only to get the token.json. 

iv token.json - File containing authorization details with Full Access Scope.

Now you are ready to run thuppu. :) 


