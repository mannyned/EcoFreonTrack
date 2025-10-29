@echo off
echo Stopping Flask processes...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *app.py*" 2>nul
timeout /t 3 /nobreak >nul

echo Deleting old database files...
del /F /Q "C:\Users\Manny\EcoFreonTrack\instance\*.db" 2>nul
timeout /t 1 /nobreak >nul

echo Starting EcoFreonTrack...
cd "C:\Users\Manny\EcoFreonTrack"
python app.py
