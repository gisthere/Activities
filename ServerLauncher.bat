@echo off
SET _serverPath=.\Activities\manage.py
SET _addr=localhost
SET _port=666
SET _pythonPath=.\venv\Scripts\python

%_pythonPath% %_serverPath% makemigrations
%_pythonPath% %_serverPath% migrate
%_pythonPath% %_serverPath% runserver %_addr%:%_port%