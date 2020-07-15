

pip freeze to get requirements file

REQUIRMENTS:
1. python 3+
2. pip3

WINDOWS:
Open the terminal in the folder with README.txt:
1. have the folder open that has the README.txt 
2. press 'shift + right click' anyhwere
3. select "Open PowerShell window here"

First time running the program, open the terminal in the folder with README.txt and run the following commands:
1. python3 -m pip install pip
2. pip3 install --user virtualenv
3. py -m venv env
4. .\env\Scripts\activate
5. pip3 install -r requirements.txt
6. python website.py

Then afterwards you just have to open the terminal in the folder wiht README.txt and run the following commands:
1. .\env\Scripts\activate
2. python website.py

MAC:
Open the terminal in the folder with README.txt:
1. open a seperate terminal
2. drag and drop onto the terminal the folder named "study_help-master" that has this readme.txt in it

First time running the program, open the terminal in the folder with README.txt and run the following commands:
1. pip3 install pip --upgrade
2. pip3 install pipenv --upgrade
3. pipenv install
4. pipenv shell
5. pip3 install -r requirements.txt
6. python3 website.py

Then afterwards you just have to open the terminal in the folder wiht README.txt and run the following commands:
1. pipenv shell
2. python3 website.py
