@echo off

:: GetAdminRules
REM --> Check for permissions
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

REM --> If error flag set, we do not have admin.
if %errorlevel% neq 0 (
    echo Requesting administrative privileges...
    goto UACPrompt
) else (goto gotAdmin)

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    if exist "%temp%\getadmin.vbs" del "%temp%\getadmin.vbs"

:: Main script
set "CURRENT_FOLDER=%~dp0"
set "PYTHON_VERSION=3.11.5"
set "PYTHON_INSTALLER_DIR=%CURRENT_FOLDER%\resources\installer"
set "PYTHON_INSTALLER=%PYTHON_INSTALLER_DIR%\python-%PYTHON_VERSION%.exe"
::
echo Python installer found: %PYTHON_INSTALLER%

echo Installing Python %PYTHON_VERSION%, it will take some time, please wait. Thank you for patience...

start /wait "" "%PYTHON_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1

echo Python installation complete!!!!.

:: Switch to pip/libs installer
echo Switch to libs and pip installer
timeout /t 3 /nobreak >nul
call "%PYTHON_INSTALLER_DIR%\install-pip-libs.bat"

exit
