@echo off
title Simple ERP Server
echo Starting Simple ERP Server...
python -c "exec(open('run.py').read())" & taskkill /F /IM python.exe > nul 2>&1
pause
