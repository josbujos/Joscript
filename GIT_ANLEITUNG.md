# 🚀 Git-Anleitung für JosScript

## 📋 Übersicht der Branches

Dein JosScript-Repository hat jetzt **zwei Hauptbranches**:

- **`windows-main`** 🪟 - Windows-Version mit .bat Dateien
- **`linux-main`** 🐧 - Linux-Version mit .sh Skripten und venv

## 🔄 Zwischen Branches wechseln

### Zu Windows-Branch wechseln
```bash
git checkout windows-main
```

### Zu Linux-Branch wechseln
```bash
git checkout linux-main
```

### Aktuellen Branch anzeigen
```bash
git branch
# Der aktuelle Branch wird mit * markiert
```

## 📁 Was ist in welchem Branch?

### 🪟 Windows-Branch (`windows-main`)
- `agent_simple.py` - Hauptprogramm
- `install.bat` - Windows-Installer
- `install_joscript.bat` - JosScript-Installer
- `start_josscript.bat` - JosScript-Starter
- `requirements.txt` - Windows-Dependencies
- `README.md` - Windows-Dokumentation

### 🐧 Linux-Branch (`linux-main`)
- `agent_simple.py` - Hauptprogramm (gleich)
- `install_josscript.sh` - Linux-Installer
- `start_josscript.sh` - Linux-Starter
- `requirements_linux.txt` - Linux-Dependencies
- `venv_linux/` - Virtual Environment
- `README_LINUX.md` - Linux-Dokumentation
- `LINUX_SETUP_COMPLETE.md` - Setup-Status

## 🚀 Häufige Git-Befehle

### Status prüfen
```bash
git status
```

### Änderungen anzeigen
```bash
git diff
```

### Alle Branches anzeigen
```bash
git branch -a
```

### Neuen Branch erstellen
```bash
git checkout -b neuer-branch-name
```

### Branch löschen
```bash
git branch -d branch-name
```

## 💡 Tipps

1. **Immer vor dem Wechseln committen** - Speichere deine Änderungen!
2. **Branch-Namen merken** - `windows-main` und `linux-main`
3. **Bei Unsicherheit**: `git status` zeigt den aktuellen Zustand
4. **Bei Problemen**: `git checkout linux-main` bringt dich zurück zum Linux-Branch

## 🔧 Beispiel-Workflow

```bash
# 1. Aktuellen Branch prüfen
git branch

# 2. Zu Windows-Branch wechseln (für Windows-Entwicklung)
git checkout windows-main

# 3. Änderungen machen und committen
git add .
git commit -m "🪟 Windows-Feature hinzugefügt"

# 4. Zurück zu Linux-Branch
git checkout linux-main

# 5. Linux-Entwicklung fortsetzen
```

## 🆘 Hilfe bei Problemen

### Alle lokalen Änderungen verwerfen
```bash
git reset --hard HEAD
```

### Zu letztem Commit zurückkehren
```bash
git checkout .
```

### Remote-Repository aktualisieren
```bash
git fetch origin
git pull origin linux-main  # oder windows-main
```

---

**💡 Merke**: Du kannst jetzt problemlos zwischen Windows- und Linux-Entwicklung wechseln!
