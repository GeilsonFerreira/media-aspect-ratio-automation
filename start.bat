@echo off

REM Ativar ambiente virtual
call .venv\Scripts\activate.bat

REM Executar o script Python
python videodesfoc.py

REM Manter o prompt aberto após execução
pause
