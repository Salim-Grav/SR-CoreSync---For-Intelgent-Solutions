@echo off
title S&R CloudPOS Connector Agent
echo Starting S&R CloudPOS Connector Service...
python "%~dp0pos_agent.py"
pause
