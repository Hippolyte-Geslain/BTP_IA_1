@echo off
cd /d "%~dp0"
echo Adding test users to database...
python add_users.py
pause
