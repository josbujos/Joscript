# JosScript - Lokaler AI Code Editor mit Blockchain

🤖 **JosScript** ist ein fortschrittlicher lokaler AI-Code-Editor, der StarCoder2 mit TensorRT-Optimierung und Blockchain-Integration verwendet.

> **Hinweis:**
> - Das große StarCoder2 Modell (`starcoder2-15b-Q5_K_S.gguf`) **ist nicht im Repository enthalten** und muss separat heruntergeladen werden (siehe unten).
> - Auch der gesamte `llama-cpp-python/` Ordner (enthält die Backend-Bibliothek für lokale Inferenz) **ist nicht im Repository** und muss separat gebaut oder bezogen werden.

## ✨ Features

- 🧠 **StarCoder2 Integration**: Lokale AI-Code-Generierung ohne Cloud-Abhängigkeit
- ⚡ **TensorRT Optimierung**: GPU-Beschleunigung für RTX 50xx Karten
- 🔗 **Blockchain-Integration**: Code-Änderungen werden in einer Blockchain gespeichert
- 📁 **Intelligente Ordnerverarbeitung**: Unterstützt 70+ Dateitypen mit Unterordner-Rekursion
- 🎨 **Moderne GUI**: Verschiebbare Bereiche, Tooltips, farbliche Kategorien
- 🔍 **Code-Analyse**: Automatische Pattern-Erkennung und Best Practices
- 💾 **Sichere Backups**: Automatische Sicherung vor Code-Ersetzungen

## 🚀 Installation

### Voraussetzungen
- Windows 10/11
- NVIDIA RTX 50xx GPU (empfohlen)
- Python 3.11+
- 16GB+ RAM
- 20GB+ freier Speicherplatz

### Schnellstart
```bash
# 1. Repository klonen
git clone https://github.com/yourusername/josscript.git
cd josscript

# 2. Installation starten
install_josscript.bat

# 3. JosScript starten
start_josscript.bat
```

### Manuelle Installation
```bash
# Virtual Environment erstellen
python -m venv josscript_env
josscript_env\Scripts\activate

# Dependencies installieren
pip install -r requirements.txt

# StarCoder2 Modell herunterladen (separat)
# Download: starcoder2-15b-Q5_K_S.gguf (10GB)
# Link: https://huggingface.co/TheBloke/starcoder2-15B-GGUF

# llama-cpp-python Backend (separat)
# Entweder selbst bauen (https://github.com/abetlen/llama-cpp-python) oder passende Windows-Binaries verwenden

# JosScript starten
python agent_simple.py
```

## 📁 Projektstruktur

```
josscript/
├── agent_simple.py          # Hauptanwendung
├── requirements.txt         # Python Dependencies
├── install_josscript.bat    # Windows Installer
├── start_josscript.bat      # Windows Starter
├── README.md               # Diese Datei
├── LICENSE                 # MIT Lizenz
├── .gitignore             # Git Ignore Regeln
├── starcoder2-15b-Q5_K_S.gguf  # AI Modell (10GB, separat, nicht im Repo)
├── llama-cpp-python/           # Backend-Bibliothek (separat, nicht im Repo)
└── code_blockchain.json    # Blockchain Daten (wird erstellt)
```

## 🎯 Verwendung

### 1. Code laden
- **📁 Datei laden**: Einzelne Datei öffnen
- **📁 Ordner laden**: Alle Dateien aus Ordner + Unterordner laden
- **🤖 JosScript laden**: JosScript selbst laden

### 2. AI verwenden
- **🔵 Code einfügen**: AI-Code direkt in Editor einfügen (grün markiert)
- **🔵 Agent**: AI-Antwort nur anzeigen
- **🟣 Analysieren**: Code-Struktur und Patterns analysieren
- **🟣 Verbessern**: Code-Optimierungen vorschlagen
- **🟣 Erweitern**: Neue Features hinzufügen

### 3. Blockchain
- **🟠 Blockchain Status**: Aktuelle Blockchain anzeigen
- **🟠 Auto-Verarbeitung**: Alle Python-Dateien automatisch analysieren

## 🔧 Konfiguration

### GPU-Optimierung
```python
# In agent_simple.py anpassen:
MODELLPFAD = "starcoder2-15b-Q5_K_S.gguf"
MAX_TOKENS = 2048
TEMPERATURE = 0.7
```

### Unterstützte Dateitypen
JosScript unterstützt 70+ Dateitypen:
- **Programmiersprachen**: Python, Java, C++, JavaScript, TypeScript, C#, Ruby, PHP, Go, Rust, Swift, Kotlin, Scala, Haskell, Clojure, Erlang, Elixir, Lisp, ML, F#, D, Pascal, Fortran, Ada, Julia, MATLAB, Racket, Scheme, Common Lisp, Groovy
- **Skriptsprachen**: Bash, PowerShell, Batch, VBScript
- **Konfiguration**: JSON, YAML, TOML, INI, XML, CSV, Properties, .env, .gitignore
- **Dokumentation**: Markdown, Text, RST, AsciiDoc, LaTeX, Word
- **Web**: HTML, CSS, SCSS, SASS, LESS, Vue, Svelte
- **Datenbank**: SQL, SQLite
- **Build**: Dockerfile, Makefile, CMake, Gradle, Maven, .sln, .vcxproj, .csproj, .xcodeproj

## 🎨 GUI Features

### Farbkategorien
- 🟢 **Grün**: Datei-Operationen (Laden, Speichern)
- 🔵 **Blau**: AI-Funktionen (Agent, Code einfügen)
- 🟣 **Lila**: Code-Analyse (Analysieren, Verbessern, Erweitern)
- 🟠 **Orange**: Blockchain (Status, Auto-Verarbeitung)

### Verschiebbare Bereiche
- **Editor**: Code-Bearbeitung (links)
- **AI-Buttons**: Funktionen (mitte)
- **Konsole**: Ausgabe und Blockchain (unten)

## 🔗 Blockchain

JosScript verwendet eine lokale Blockchain für:
- **Code-Änderungen verfolgen**: Alle AI-generierten Änderungen
- **Versionierung**: Automatische Backups vor Ersetzungen
- **Transparenz**: Vollständige Historie aller Aktionen
- **Sicherheit**: Hash-basierte Integritätsprüfung

## 🚀 Performance

### RTX 50xx Optimierung
- **TensorRT 10.12.0.36**: GPU-Beschleunigung
- **Flash Attention 2.7.4**: Optimierte Attention-Mechanismen
- **3-5x Speedup**: Gegenüber CPU-only Ausführung
- **Batch-Größe 512**: Optimiert für RTX 50xx

### Speicherverbrauch
- **Modell**: ~10GB VRAM (StarCoder2 15B)
- **System**: ~4GB RAM
- **Blockchain**: ~1MB pro 1000 Aktionen

## 🛠️ Entwicklung

### Beitragen
1. Fork das Repository
2. Feature Branch erstellen (`git checkout -b feature/AmazingFeature`)
3. Änderungen committen (`git commit -m 'Add AmazingFeature'`)
4. Branch pushen (`git push origin feature/AmazingFeature`)
5. Pull Request erstellen

### Lokale Entwicklung
```bash
# Development Environment
python -m venv dev_env
dev_env\Scripts\activate
pip install -r requirements.txt

# Tests ausführen
python -m pytest tests/

# Code formatieren
black agent_simple.py
```

## 📄 Lizenz

Dieses Projekt steht unter der MIT Lizenz - siehe [LICENSE](LICENSE) Datei für Details.

## 🙏 Danksagungen

- **StarCoder2**: BigCode für das AI-Modell
- **llama.cpp**: Für die lokale Inferenz
- **TensorRT**: NVIDIA für GPU-Optimierung
- **Hugging Face**: Für Modell-Hosting

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/josscript/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/josscript/discussions)
- **Wiki**: [GitHub Wiki](https://github.com/yourusername/josscript/wiki)

---

⭐ **Star das Repository** wenn es dir gefällt! 