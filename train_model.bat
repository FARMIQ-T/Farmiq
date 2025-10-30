@echo off
cd /d %~dp0
call .venv\Scripts\activate.bat
python ai-models\cron_training.py >> logs\cron.log 2>&1
deactivate