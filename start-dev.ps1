$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$backend = Join-Path $root 'Back-end'
$frontend = Join-Path $root 'Front-end'

function Test-PortInUse([int]$port) {
	return [bool](Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue)
}

if (-not (Test-PortInUse 8000)) {
	Start-Process powershell -WorkingDirectory $backend -ArgumentList '-NoExit', '-Command', 'python manage.py runserver 127.0.0.1:8000'
} else {
	Write-Host 'Backend já está rodando na porta 8000.' -ForegroundColor Yellow
}

if (-not (Test-PortInUse 4200)) {
	Start-Process powershell -WorkingDirectory $frontend -ArgumentList '-NoExit', '-Command', 'npm start'
} else {
	Write-Host 'Frontend já está rodando na porta 4200.' -ForegroundColor Yellow
}

Write-Host 'SpaceGames iniciado.' -ForegroundColor Green
Write-Host 'Frontend: http://localhost:4200/'
Write-Host 'API Django: http://127.0.0.1:8000/api/'
