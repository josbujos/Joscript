@echo off
echo ========================================
echo JosScript - Installation
echo ========================================
echo.

REM Prüfe ob Python installiert ist
python --version >nul 2>&1
if errorlevel 1 (
    echo FEHLER: Python ist nicht installiert!
    echo Bitte installieren Sie Python 3.11+ von https://python.org
    pause
    exit /b 1
)

echo Python gefunden: 
python --version

REM Erstelle virtuelles Environment
echo.
echo Erstelle virtuelles Environment...
if not exist "josscript_env" (
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

REM Installiere PyTorch mit CUDA 12.9 Support
echo.
echo Installiere PyTorch mit CUDA 12.9 Support...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu129

REM Installiere llama-cpp-python mit CUDA Support
echo.
echo Installiere llama-cpp-python mit CUDA Support...
pip install llama-cpp-python --force-reinstall --index-url https://jllllll.github.io/llama-cpp-python-cuBLAS-wheels/cu129

REM Installiere alle anderen Pakete aus requirements.txt
echo.
echo Installiere alle JosScript Abhängigkeiten...
pip install -r requirements.txt

echo.
echo ========================================
echo Installation abgeschlossen!
echo ========================================
echo.
echo Um JosScript zu starten:
echo 1. start_josscript.bat ausführen
echo 2. Oder: josscript_env\Scripts\activate.bat
echo    Dann: python agent_simple.py
echo.
pause 