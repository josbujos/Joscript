# JosScript - Linux Version

🤖 **JosScript** ist ein fortschrittlicher lokaler AI-Code-Editor, der StarCoder2 mit Blockchain-Integration verwendet.

## 🐧 Linux Installation

### Voraussetzungen
- Ubuntu 20.04+ oder Debian 11+
- Python 3.11+
- 8GB+ RAM
- 10GB+ freier Speicherplatz

### Schnellstart

#### 1. Repository klonen
```bash
git clone https://github.com/josbujos/Joscript.git
cd Joscript
```

#### 2. Automatische Installation
```bash
# Mache Installer ausführbar
chmod +x install_joscript.sh

# Führe Installation aus
./install_josscript.sh
```

#### 3. JosScript starten
```bash
# Mit Start-Skript
./start_josscript.sh

# Oder manuell
source venv_linux/bin/activate
python agent_simple.py
```

### Manuelle Installation

#### 1. System-Dependencies installieren
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

#### 2. Virtual Environment erstellen
```bash
python3 -m venv venv_linux
source venv_linux/bin/activate
pip install --upgrade pip
```

#### 3. Dependencies installieren
```bash
# Core Dependencies
pip install numpy requests tqdm colorama psutil

# AI Dependencies
pip install llama-cpp-python

# Zusätzliche Dependencies
pip install jinja2 markupsafe diskcache
```

## 🚀 Verwendung

### StarCoder2 Modell herunterladen
Das AI-Modell ist nicht im Repository enthalten und muss separat heruntergeladen werden:

```bash
# Download von Hugging Face
# https://huggingface.co/TheBloke/starcoder2-15B-GGUF
# Datei: starcoder2-15b-Q5_K_S.gguf

# Oder mit wget (falls installiert):
wget https://huggingface.co/TheBloke/starcoder2-15B-GGUF/resolve/main/starcoder2-15b-Q5_K_S.gguf
```

### Features
- 🧠 **StarCoder2 Integration**: Lokale AI-Code-Generierung
- 🔗 **Blockchain-Integration**: Code-Änderungen werden verfolgt
- 📁 **Intelligente Ordnerverarbeitung**: Unterstützt 70+ Dateitypen
- 🎨 **Moderne GUI**: Tkinter-basierte Benutzeroberfläche
- 🔍 **Code-Analyse**: Automatische Pattern-Erkennung

## 📁 Projektstruktur

```
josscript/
├── agent_simple.py          # Hauptanwendung
├── requirements_linux.txt   # Linux Dependencies
├── install_josscript.sh     # Linux Installer
├── start_josscript.sh       # Linux Starter
├── venv_linux/              # Virtual Environment
├── frühereDaten/            # Backup-Ordner
├── README_LINUX.md          # Diese Datei
└── starcoder2-15b-Q5_K_S.gguf  # AI Modell (separat)
```

## 🔧 Konfiguration

### GPU-Optimierung (optional)
Für NVIDIA GPUs können zusätzliche Optimierungen installiert werden:

```bash
# CUDA Support für llama-cpp-python
pip install llama-cpp-python --force-reinstall --index-url https://jllllll.github.io/llama-cpp-python-cuBLAS-wheels/cu118

# TensorRT (nur mit NVIDIA GPU)
# https://developer.nvidia.com/tensorrt
```

### Modell-Pfad anpassen
In `agent_simple.py` den Modell-Pfad anpassen:

```python
MODELLPFAD = "starcoder2-15b-Q5_K_S.gguf"
```

## 🐛 Fehlerbehebung

### Tkinter Fehler
```bash
# Falls Tkinter nicht funktioniert:
sudo apt install python3-tk
```

### Import Fehler
```bash
# Virtual Environment neu aktivieren:
source venv_linux/bin/activate

# Dependencies neu installieren:
pip install -r requirements_linux.txt
```

### Speicher-Probleme
```bash
# Modell-Größe reduzieren:
# Verwende starcoder2-7b-Q4_K_M.gguf statt 15b
```

## 📊 Performance

### System-Anforderungen
- **Minimal**: 8GB RAM, CPU-only
- **Empfohlen**: 16GB RAM, NVIDIA GPU
- **Optimal**: 32GB RAM, RTX 40xx/50xx

### Geschwindigkeit
- **CPU-only**: 2-5 Tokens/Sekunde
- **GPU (CUDA)**: 10-50 Tokens/Sekunde
- **GPU (TensorRT)**: 20-100 Tokens/Sekunde

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/josbujos/Joscript/issues)
- **Linux-spezifische Probleme**: Erwähne "Linux" in der Issue-Beschreibung

## 📄 Lizenz

MIT Lizenz - siehe [LICENSE](LICENSE) Datei für Details.

---

⭐ **Star das Repository** wenn es dir gefällt!
