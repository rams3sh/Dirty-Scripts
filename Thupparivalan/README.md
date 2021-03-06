Thupparivalan (Thuppu - Shortform)
----------------------------------

Thupparivalan in tamil means "Detective".

The script was written mainly for a daily task where I would have to take the diff of the changed files or folders within a specific parent folder in google drive and analyze for the content. 

This script identifies the changed files alone (created or modified and not deleted items) and downloads to a folder with "Evidence-<DD-MM-YYYY_HH-MM-SS>" naming convention within the same folder as Thupparivalan. This was needed as it was a big headache to identify the changed files/ folders manually and download one by one.


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

i. thupparivalan.py  - The main script 

ii. thuppu.config - The config file for the tool

iii. credentials.json - File containing your credential tokens/secrets required to get authorization token for querying and fetching files using google drive api 

For iii. above, follow the below steps 

Step 1: Go to https://developers.google.com/drive/api/v3/quickstart/python

Step 2: Follow till all steps within  "Step 1: Turn on the Drive API".

Step 3: Copy the downloaded credentials.json in the same folder as thupparivalan and run !!


Set the PARENT_FOLDER_NAME and PARENT_FOLDER_ID in the thuppu.config file.
For how to's of  finding folder ID  go to :-
"https://googleappsscriptdeveloper.wordpress.com/2017/03/04/how-to-find-your-google-drive-folder-id/"

Post all the steps above, you would be required to create token.json file which will have the authorizing details for thuppu to use google drive api using your credentials. Need not bother about it, if this file is not in path , thuppu will automatically guide you in creating one.

Refer :https://developers.google.com/drive/api/v3/about-auth for more details about the token. Please note by default the scope of the token is "https://www.googleapis.com/auth/drive" which is equivalent of Full access to your drive. I have used this scope to avoid any permission related errors.


Finally you will have 4 files in your folder :-

i. thupparivalan.py  - The main script

ii. thuppu.config - The config file for the tool with all the parameters set.

iii. credentials.json - File containing your credentials / secret token to get authrization token. Not required anymore as it is required only during intial steps to get the token.json. 

iv token.json - File containing authorization details with Full Access Scope.

Now you are ready to run thuppu. :) 


Working 
--------

Each time when Thuppu is run, it creates a state file where it records the entire tree structure of the parent folder.When it is run the next time , it again records the current state of the folder tree structure and diffs between the laststate and current state to identify all the changed files.

Through this identification, it takes all the fileID (Google Drive reference to identify given folder/file) of each of the changed file and downloads them in the same folder structure within a newly created folder with naming convention of "Evidence-<DD-MM-YYYY_HH-MM-SS>". 

Note:
-----

In case you want to delegate the work to next person to check on the states post the one you have checked last, you would have to provide him/her with your "laststate.txt" file which he/she need to have it in their current directory path. In case if he/she uses a different OS from yours , then the laststate file needs to modified little bit before hand over. Reason given below.

If you are using Linux or Mac , the last state file will have filepath something like this -  "\parentfolder\testfolder\file".
If you are using windows , the last state file will have filepath something like this - "parentfolder/testfolder/file". Note the difference in path character. This is because of difference in how each type of OS refers file path.

So directly using your laststate file with thuppu onto a person's system with different OS other than yours will result in thuppu seeing all the files in the drive as new compared to the laststate resulting in complete download of the root folder contents because of the character change in the files' /folders' path. 

And this is not desired outcome. Hence , you need to convert your laststate.txt file to a compatible laststate file for the concerned person's os.

You can use the laststate converter named "kaima-thuppu.py" for this. 

Let's say your OS is windows and the other person's os is mac.
Then you execute the following command :-

-> python kaima-thuppu.py mac laststate.txt

This will give a new file called laststate_mac.txt. Send this file to the other person.
The next person should rename this file to laststate.txt and place it in the same folder as Thupparivalan tool. And now , he /she is ready to run the tool for tracking and downloading further changes in the drive.
