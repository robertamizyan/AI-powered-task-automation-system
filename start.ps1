Write-Host "Starting AI Task Bot..." -ForegroundColor Green

$projectPath = "C:\Users\Rob\Desktop\ai-task-bot"
$redisPath = "C:\Program Files\Redis"

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$redisPath'; .\redis-server.exe --port 6380"

Start-Sleep -Seconds 2

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectPath\backend'; .\.venv\Scripts\activate; uvicorn main:app --reload"

Start-Sleep -Seconds 2

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectPath\worker'; .\.venv\Scripts\activate; python worker.py"

Start-Sleep -Seconds 2

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectPath\bot'; .\.venv\Scripts\activate; python bot.py"

Start-Sleep -Seconds 2

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectPath\frontend'; npm run dev"

Write-Host "All services started." -ForegroundColor Green
Write-Host "Open dashboard: http://localhost:5173" -ForegroundColor Yellow