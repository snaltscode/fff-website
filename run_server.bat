@echo off
title Founder for Founder Server
cd /d "%~dp0"

echo =======================================================
echo   FOUNDER FOR FOUNDER - MEMBERSHIP & WEB PLATFORM
echo =======================================================
echo.
echo [1/2] Opening browser to http://localhost:8000 ...
timeout /t 1 /nobreak >nul
start http://localhost:8000

echo [2/2] Launching Python backend server on port 8000 ...
echo.
echo Admin Login Credentials:
echo   Email: admin@founderforfounder.in
echo   Password: Admin@123
echo.
echo -------------------------------------------------------
echo  Server is running! Keep this window open while using the app.
echo  (Press Ctrl+C to stop the server)
echo -------------------------------------------------------
echo.

python server.py
if errorlevel 1 (
    echo.
    echo [ERROR] Python server failed to start or Python was not found in PATH.
    echo Please make sure Python 3 is installed and added to PATH.
    pause
)
