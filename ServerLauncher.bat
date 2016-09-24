@echo off
SET _serverPath=.\Activities\manage.py
SET _addr=localhost
SET _port=666

python %_serverPath% makemigrations
python %_serverPath% migrate
python %_serverPath% runserver %_addr%:%_port%