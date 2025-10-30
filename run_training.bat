@echo off
setlocal enabledelayedexpansion

:: Set paths
set BASE_DIR=%~dp0
set VENV_DIR=%BASE_DIR%.venv
set PYTHON=%VENV_DIR%\Scripts\python.exe
set SCRIPT_PATH=%BASE_DIR%ai-models\cron_training.py
set LOG_DIR=%BASE_DIR%logs
set LOG_FILE=%LOG_DIR%\cron_%date:~-4,4%%date:~-10,2%%date:~-7,2%.log

:: Create logs directory if it doesn't exist
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

:: Log start time
echo [%date% %time%] Starting model training >> "%LOG_FILE%"

:: Check if Python virtual environment exists
if not exist "%PYTHON%" (
    echo [%date% %time%] ERROR: Python virtual environment not found at %PYTHON% >> "%LOG_FILE%"
    exit /b 1
)

:: Activate virtual environment and run training
call "%VENV_DIR%\Scripts\activate.bat"
if %ERRORLEVEL% neq 0 (
    echo [%date% %time%] ERROR: Failed to activate virtual environment >> "%LOG_FILE%"
    exit /b 1
)

:: Run the training script
"%PYTHON%" "%SCRIPT_PATH%" >> "%LOG_FILE%" 2>&1
if %ERRORLEVEL% neq 0 (
    echo [%date% %time%] ERROR: Training script failed with error code %ERRORLEVEL% >> "%LOG_FILE%"
    call "%VENV_DIR%\Scripts\deactivate.bat"
    exit /b 1
)

:: Deactivate virtual environment
call "%VENV_DIR%\Scripts\deactivate.bat"

:: Log completion
echo [%date% %time%] Model training completed successfully >> "%LOG_FILE%"

endlocal