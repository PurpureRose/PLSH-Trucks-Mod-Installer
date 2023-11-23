@echo off

set PYTHON_VERSION=3.11.5
set PYTHON_INSTALLER_DIR=resources\installer
set PYTHON_INSTALLER=%PYTHON_INSTALLER_DIR%\python-%PYTHON_VERSION%.exe

echo Installing Python %PYTHON_VERSION%, it may take a while...

rem Run the Python installer silently
start /wait %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1

echo Python installation complete.

rem Call libsinstaller
call %PYTHON_INSTALLER_DIR%\installibs.bat

rem Pause to keep the command prompt window open
pause
