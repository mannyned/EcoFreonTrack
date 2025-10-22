@echo off
REM EcoFreonTrack - Development Environment Startup Script
REM Run this script to start the application in DEVELOPMENT mode

echo ========================================
echo EcoFreonTrack - Development Mode
echo ========================================
echo.

REM Set environment to development
set FLASK_ENV=development
set FLASK_DEBUG=1

REM Display configuration
echo Environment: %FLASK_ENV%
echo Database: instance/epa608_tracker_dev.db
echo.
echo Starting development server...
echo Access at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Run the application
python app.py

pause
