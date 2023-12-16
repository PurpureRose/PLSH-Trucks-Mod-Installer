@echo off
:: Set 
set "CURRENT_FOLDER=%~dp0"
set "PYTHON_VERSION=3.11.5"
set "PYTHON_INSTALLER_DIR=%CURRENT_FOLDER%resources\installer"
set "GET_PIP_SCRIPT=%CURRENT_FOLDER%\install-pip.py"
set "GET_LIB_SCRIPT=%CURRENT_FOLDER%\install-libs.py"

:: Script
timeout /t 1 /nobreak >nul

echo Now starting pip and libraries install...

:: Wait for a few seconds
timeout /t 2 /nobreak >nul

:: Run pip installer
python "%GET_PIP_SCRIPT%"

:: Wait for a few seconds
timeout /t 3 /nobreak >nul

:: Run pip
python "%GET_LIB_SCRIPT%"
echo Install complete!

:: Pause to keep the command prompt window open
pause