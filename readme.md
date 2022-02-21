**This repo is intended for archive only there will be no follow up or questions answered.
If you're fine with that you're free to use this script** 



**Ali_Pyscrapper**
 A script who connect to alibaba via linkedin instantiate a search 
then scrap images and info found in the results page until the last page.
take the time to go through the script as some informations need to be added.

**config.py**
writte here your linkedin credential for login 


**within the script**
**Wpath**
write here the path to the chromedriver 


**searchQuery**

will be used to instantiate the search but also to generate a path for a future created directory and the Json file with some function within the script.

**path_dir** 
inform here the full path to the Ali scrapper script this will be used to create a directory who will recieve the downloaded images and the json file to keep things organized.


**Before the first run**
safer to run within a virtualenv:
**with a terminal** 
cd /path_to_script/ALi_Pyscrapper.py 
**generate the virtual environnement**
virtualenv venv 
**activate the virtual environement**
source venv/bin/activate | your should see (venv)on your terminal 
**install depedency**
pip3 install -r requirements.txt 
**run the script**
python3 Ali_Pyscrapper.py 
