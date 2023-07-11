@echo off
:1
python3 updater.py
if errorlevel 0 (
	exit
)
goto 1
