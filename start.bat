@echo off
echo Iniciando Media Aspect Ratio Automation...

REM Ir para a pasta do projeto (onde está este .bat)
cd /d %~dp0

REM Ativar ambiente virtual
call .venv\Scripts\activate.bat

REM Executar o projeto
python src\main.py

REM Manter o prompt aberto
pause
