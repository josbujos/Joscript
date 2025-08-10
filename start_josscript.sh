#!/bin/bash

# JosScript - Linux Starter Script
# Startet JosScript mit aktiviertem Virtual Environment

echo "🚀 Starte JosScript für Linux..."
echo "📁 Aktueller Pfad: $(pwd)"

# Prüfe ob venv existiert
if [ ! -d "venv_linux" ]; then
    echo "❌ Virtual Environment 'venv_linux' nicht gefunden!"
    echo "💡 Führe zuerst 'install_josscript.sh' aus"
    exit 1
fi

# Aktiviere Virtual Environment
echo "🔧 Aktiviere Virtual Environment..."
source venv_linux/bin/activate

# Prüfe ob Python-Dependencies installiert sind
if ! python -c "import tkinter, numpy, requests" 2>/dev/null; then
    echo "❌ Nicht alle Dependencies sind installiert!"
    echo "💡 Führe zuerst 'install_josscript.sh' aus"
    exit 1
fi

# Prüfe ob das StarCoder2 Modell existiert
if [ ! -f "starcoder2-15b-Q5_K_S.gguf" ]; then
    echo "⚠️  StarCoder2 Modell nicht gefunden!"
    echo "💡 Lade das Modell von: https://huggingface.co/TheBloke/starcoder2-15B-GGUF"
    echo "📁 Datei: starcoder2-15b-Q5_K_S.gguf"
    echo ""
    echo "🔄 Starte JosScript im Demo-Modus (ohne AI)..."
    echo "💡 AI-Funktionen werden nicht funktionieren bis das Modell geladen ist"
fi

# Starte JosScript
echo "🤖 Starte JosScript..."
python agent_simple.py

# Deaktiviere Virtual Environment beim Beenden
deactivate
echo "👋 JosScript beendet"
