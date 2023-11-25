@echo off

set PYTHON_VERSION=3.11.5
set PYTHON_INSTALLER_DIR=resources\installer
set PYTHON_INSTALLER=%PYTHON_INSTALLER_DIR%\python-%PYTHON_VERSION%.exe
set GET_PIP_SCRIPT=install-pip-and-libs.py

echo Installing Python %PYTHON_VERSION%, it may take a while...

rem Run the Python installer silently
start /wait %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1

echo Python installation complete.

echo Starting pip and libraies install..

rem Run pip
%PYTHON_INSTALLER_DIR%\python.exe %GET_PIP_SCRIPT%

echo Install complete!

rem Pause to keep the command prompt window open
pause
