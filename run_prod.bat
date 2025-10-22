@echo off
REM EcoFreonTrack - Production Environment Startup Script
REM Run this script to start the application in PRODUCTION mode

echo ========================================
echo EcoFreonTrack - Production Mode
echo ========================================
echo.

REM Set environment to production
set FLASK_ENV=production
set FLASK_DEBUG=0

REM Check if SECRET_KEY is set
if "%SECRET_KEY%"=="" (
    echo WARNING: SECRET_KEY environment variable is not set!
    echo Please set a secure secret key before running in production.
    echo Example: set SECRET_KEY=your-very-long-random-secret-key-here
    echo.
    echo Press any key to continue anyway (NOT RECOMMENDED) or Ctrl+C to exit...
    pause
)

REM Display configuration
echo Environment: %FLASK_ENV%
echo Database: instance/epa608_tracker_prod.db
echo.
echo Starting production server...
echo Access at: http://localhost:5000
echo.
echo IMPORTANT: For production deployment, use a WSGI server like Gunicorn or Waitress
echo This development server is NOT suitable for production use!
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Run the application
python app.py

pause
