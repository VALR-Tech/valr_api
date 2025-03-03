@echo off
.venv\Scripts\python.exe -m pytest --cov=valr_api tests/ %* 