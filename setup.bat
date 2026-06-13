@echo off
REM ============================================================================
REM ProjectMaker - Windows Setup Script
REM Project: SocialBunny
REM ============================================================================

echo Starting setup for SocialBunny...


echo Setting up Python backend...
cd backend
python -m venv venv
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

cd ..

echo Setting up frontend...
cd frontend
npm install
cd ..

echo.
echo Setup Complete!
echo.
pause
