#!/bin/bash

# JosScript - Linux Installer Script
# Installiert alle Dependencies und richtet das Projekt ein

echo "🔧 JosScript Linux Installer"
echo "================================"

# Prüfe ob Python3 installiert ist
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 ist nicht installiert!"
    echo "💡 Installiere Python3 mit: sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

# Prüfe ob pip installiert ist
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 ist nicht installiert!"
    echo "💡 Installiere pip3 mit: sudo apt install python3-pip"
    exit 1
fi

echo "✅ Python3 und pip3 sind installiert"
echo "🐍 Python Version: $(python3 --version)"
echo "📦 pip Version: $(pip3 --version)"

# Erstelle Virtual Environment
echo ""
echo "🔧 Erstelle Virtual Environment..."
if [ -d "venv_linux" ]; then
    echo "⚠️  Virtual Environment existiert bereits"
    read -p "🗑️  Überschreiben? (j/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Jj]$ ]]; then
        echo "🗑️  Lösche altes Virtual Environment..."
        rm -rf venv_linux
    else
        echo "💡 Verwende bestehendes Virtual Environment"
    fi
fi

if [ ! -d "venv_linux" ]; then
    echo "📁 Erstelle neues Virtual Environment..."
    python3 -m venv venv_linux
    if [ $? -ne 0 ]; then
        echo "❌ Fehler beim Erstellen des Virtual Environment!"
        echo "💡 Installiere python3-venv: sudo apt install python3-venv"
        exit 1
    fi
fi

# Aktiviere Virtual Environment
echo "🔧 Aktiviere Virtual Environment..."
source venv_linux/bin/activate

# Upgrade pip
echo "📦 Upgrade pip..."
pip install --upgrade pip

# Installiere Core Dependencies
echo ""
echo "📦 Installiere Core Dependencies..."
pip install numpy requests tqdm colorama psutil

# Installiere AI Dependencies
echo ""
echo "🤖 Installiere AI Dependencies..."
pip install llama-cpp-python

# Installiere zusätzliche Dependencies
echo ""
echo "🔧 Installiere zusätzliche Dependencies..."
pip install jinja2 markupsafe diskcache

# Mache Start-Skript ausführbar
echo ""
echo "🔧 Mache Start-Skript ausführbar..."
chmod +x start_josscript.sh

echo ""
echo "✅ Installation abgeschlossen!"
echo ""
echo "🚀 Nächste Schritte:"
echo "1. Lade das StarCoder2 Modell herunter:"
echo "   https://huggingface.co/TheBloke/starcoder2-15B-GGUF"
echo "   Datei: starcoder2-15b-Q5_K_S.gguf"
echo ""
echo "2. Starte JosScript:"
echo "   ./start_josscript.sh"
echo ""
echo "3. Oder manuell:"
echo "   source venv_linux/bin/activate"
echo "   python agent_simple.py"
echo ""
echo "💡 Hilfe: ./start_josscript.sh --help"

# Deaktiviere Virtual Environment
deactivate
