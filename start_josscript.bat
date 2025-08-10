@echo off
echo ========================================
echo JosScript - AI Code Editor
echo ========================================
echo.

REM Prüfe ob virtuelles Environment existiert (versuche beide Namen)
if exist "josscript_rtx5070ti_env" (
    set VENV_NAME=josscript_rtx5070ti_env
    echo Verwende existierendes Environment: josscript_rtx5070ti_env
) else if exist "josscript_env" (
    set VENV_NAME=josscript_env
    echo Verwende existierendes Environment: josscript_env
) else (
    echo FEHLER: Kein virtuelles Environment gefunden!
    echo Bitte führen Sie zuerst install_josscript.bat aus.
    pause
    exit /b 1
)

REM Aktiviere Environment
echo.
echo Aktiviere virtuelles Environment...
call %VENV_NAME%\Scripts\activate.bat

REM Prüfe GPU Support
echo.
echo Prüfe GPU Support...
python -c "import torch; print(f'CUDA verfügbar: {torch.cuda.is_available()}'); print(f'CUDA Version: {torch.version.cuda}'); print(f'Anzahl GPUs: {torch.cuda.device_count()}')"

REM Starte JosScript
echo.
echo Starte JosScript...
python agent_simple.py

pause 