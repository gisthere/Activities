--------------------------------
WINDOWS DEVELOPERS ARE WELCOME THIS SECTION
--------------------------------
So guys if you have python, or pip or django please proceed further
1) Install Python
	1.1) go to https://www.python.org/downloads/
	1.2) download python 3.5.2 and install
2) install pip
	2.1) Copy this file https://bootstrap.pypa.io/get-pip.py
	2.2) python %PATH_TO_GET-PIP.PY_FROM_2.1%/get-pip.py
3) install django
	2.2) pip install Django==1.10.2
4) Install git
	4.1) proceed to https://git-scm.com/
	4.2) download and install it
5) Install additional stuff for heroku and stuff
	5.1) pip install dj_database_url
	5.2) pip install whitenoise
	5.3) pip install psycopg2
6) Clone our repo
	6.1) run command from directory where you want to be files of project "git clone https://github.com/MSD-GroupI/Activities.git"
7) If it your first run you should use some stuff like this
	7.1) "python ./Activities/manage.py createsuperuser", creates your user at heroku.com
8) Run script ServerLauncher.bat
------------------------------------------------------------------------------
UNIX LIKE SECTION
------------------------------------------------------------------------------
1) Install git
	1.1) proceed to https://git-scm.com/
	1.2) download and install it
2) Clone our repo
	2.1) run command from directory where you want to be files of project "git clone https://github.com/MSD-GroupI/Activities.git"	
3) If it your first run you should use some stuff like this
	3.1) "python ./Activities/manage.py createsuperuser", creates your user at heroku.com
4) "sudo chmod +x UnixRunVenv.sh"
5) "sudo ./UnixRunVenv.sh" (script for macosx that uses brew, if you are using apt-get or aptitude install you should modify scrit)

