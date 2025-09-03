@echo off
echo Starting DeepVision Research System...
echo.

echo Starting FastAPI Backend...
start "DeepVision Backend" cmd /k "cd /d %~dp0 && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && python app.py"

echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo Starting Next.js Frontend...
start "DeepVision Frontend" cmd /k "cd /d %~dp0\DeepVision && npm run dev"

echo.
echo DeepVision is starting up!
echo Backend will be available at: http://localhost:8000
echo Frontend will be available at: http://localhost:3000
echo.
echo Press any key to close this window...
pause > nul
