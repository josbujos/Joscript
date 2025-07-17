@echo off
echo ========================================
echo JosScript - Installation
echo ========================================
echo.

REM Prüfe ob Python installiert ist
python --version >nul 2>&1
if errorlevel1 (
    echo FEHLER: Python ist nicht installiert!
    echo Bitte installieren Sie Python 3.11von https://python.org
    pause
    exit /b 1
)

echo Python gefunden: 
python --version

REM Erstelle virtuelles Environment
echo.
echo Erstelle virtuelles Environment...
if not exist josscript_env" (
    python -m venv josscript_env
    echo Virtuelles Environment erstellt.
) else (
    echo Virtuelles Environment existiert bereits.
)

REM Aktiviere Environment
echo.
echo Aktiviere virtuelles Environment...
call josscript_env\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrade pip...
python -m pip install --upgrade pip

REM Installiere alle Pakete aus requirements.txt
echo.
echo Installiere JosScript Dependencies...
pip install -r requirements.txt

REM Erstelle start.bat
echo.
echo Erstelle start.bat...
(
echo @echo off
echo echo ========================================
echo echo JosScript - AI Code Editor
echo echo ========================================
echo echo.
echo echo Prüfe ob StarCoder2dell vorhanden...
echo if not exist starcoder215b-Q5_K_S.gguf ^(
echo     echo FEHLER: StarCoder2ell nicht gefunden!
echo     echo.
echo     echo Bitte laden Sie das Modell herunter:
echo     echo https://huggingface.co/TheBloke/starcoder2-15GGUF
echo     echo.
echo     echo Datei: starcoder2-15b-Q5K_S.gguf ^(10GB^)
echo     pause
echo     exit /b 1
echo ^)
echo.
echo echo Modell gefunden! Starte JosScript...
echo.
echo REM Aktiviere Environment
echo call josscript_env\Scripts\activate.bat
echo.
echo REM Starte JosScript
echo python agent_simple.py
echo.
echo pause
) > start.bat

echo.
echo ========================================
echo Installation abgeschlossen!
echo ========================================
echo.
echo Nächste Schritte:
echo1 StarCoder2dell herunterladen ^(10GB^):
echo    https://huggingface.co/TheBloke/starcoder2-GGUF
echo    Datei: starcoder2b-Q5_K_S.gguf
echo.
echo 2 JosScript starten:
echo    start.bat
echo.
echo Oder manuell:
echo    josscript_env\Scripts\activate.bat
echo    python agent_simple.py
echo.
pause 