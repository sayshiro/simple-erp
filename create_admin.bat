@echo off
title Simple ERP Admin Setup
echo Setting up administrator account...
python -c "exec(open('quick_setup_admin.py').read())"
echo.
echo Press any key to close this window...
pause > nul
