@echo off

set PYTHON_LIBRAIES=ttkbootstrap requests gdown
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