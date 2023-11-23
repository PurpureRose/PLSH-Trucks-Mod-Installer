@echo off

set PYTHON_VERSION=3.11.5
set PYTHON_INSTALLER_DIR=resources\installer
set PYTHON_INSTALLER=%PYTHON_INSTALLER_DIR%\python-%PYTHON_VERSION%.exe
set PYTHON_LIBRAIES=ttkbootstrap requests gdown

echo Installing Python %PYTHON_VERSION%...

rem Run the Python installer silently
start /wait %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1

echo Python installation complete.

echo Installing Python Libraries...

rem Check if pip is installed
where pip >nul 2>nul
if %errorlevel% neq 0 (
    echo Pip is not installed. Please install Python with pip.
    exit /b 1
)

rem Install Python packages
for %%i in (%PYTHON_LIBRAIES%) do (
    pip install %%i
    if %errorlevel% neq 0 (
        echo Failed to install package: %%i
    )
)

echo Installation completed.

rem Pause to keep the command prompt window open
pause
