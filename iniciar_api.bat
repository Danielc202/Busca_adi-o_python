@echo off
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo ERRO: Python nao foi encontrado no PATH.
    echo Instale o Python 3 e marque a opcao "Add Python to PATH".
    pause
    exit /b 1
)

python -c "import fastapi, uvicorn" >nul 2>nul
if errorlevel 1 (
    echo ERRO: dependencias nao encontradas.
    echo Execute: python -m pip install -r requirements.txt
    pause
    exit /b 1
)

echo Iniciando o servidor da API...
echo Abra no navegador: http://127.0.0.1:8000/docs
echo Para encerrar, aperte Ctrl + C nesta janela.
echo.

python -m uvicorn api:app --reload --host 127.0.0.1 --port 8000
if errorlevel 1 (
    echo.
    echo ERRO: o servidor nao conseguiu iniciar.
    echo Verifique se a porta 8000 ja esta em uso.
)
pause
