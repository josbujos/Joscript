import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText
import threading
import json
import hashlib
import time
import subprocess
import sys

# === Konfiguration ===
MODELLPFAD = "starcoder2-15b-Q5_K_S.gguf"
MAX_TOKENS = 2048
TEMPERATURE = 0.7

# === Blockchain Konfiguration ===
BLOCKCHAIN_FILE = "code_blockchain.json"
BLOCK_SIZE = 10

# === O Variablen ===
llm = None
blockchain = []
current_block = []
current_folder_info = None  # Neue Variable für Ordner-Info

# === GUI Setup ===
root = tk.Tk()
root.title("Joshuel - Starcoder2 Version mit Blockchain")
root.geometry("1400x900")
root.configure(bg="#2b2b2b")

# === Tkinter Variablen (nach root erstellt) ===
current_file_path = tk.StringVar()
agent_status = tk.StringVar(value="🟢 Bereit")

# === Styling ===
style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background="#2b2b2b")
style.configure("TButton", background="#3c3f41", foreground="white")
style.configure("TLabel", background="#2b2b2b", foreground="white")

# === Farben für Button-Kategorien ===
COLORS = {
    "file": "#4CAF50",  # Grün - Datei-Operationen
    "ai": "#2196F3",  # Blau - AI-Funktionen
    "blockchain": "#FF9800",  # Orange - Blockchain
    "code": "#9C27B0",  # Lila - Code-Analyse
    "system": "#607D8B",  # Grau - System
}


# === Blockchain Funktionen ===
def load_blockchain():
    """Lädt die Blockchain aus der Datei"""
    global blockchain
    try:
        if os.path.exists(BLOCKCHAIN_FILE):
            with open(BLOCKCHAIN_FILE, "r", encoding="utf-8") as f:
                blockchain = json.load(f)
            print(f"✅ Blockchain geladen: {len(blockchain)} Blöcke")
        else:
            blockchain = []
            print("📝 Neue Blockchain erstellt")
    except Exception as e:
        print(f"❌ Fehler beim Laden der Blockchain: {e}")
        blockchain = []


def save_blockchain():
    """Speichert die Blockchain in die Datei"""
    try:
        with open(BLOCKCHAIN_FILE, "w", encoding="utf-8") as f:
            json.dump(blockchain, f, indent=2, ensure_ascii=False)
        print("✅ Blockchain gespeichert")
    except Exception as e:
        print(f"❌ Fehler beim Speichern der Blockchain: {e}")


def add_to_blockchain(action, code_snippet, metadata=None):
    """Fügt eine Aktion zur Blockchain hinzu"""
    global current_block, blockchain

    if metadata is None:
        metadata = {}

    # Erstelle Block-Eintrag
    block_entry = {
        "timestamp": time.time(),
        "action": action,
        "code_hash": hashlib.sha256(code_snippet.encode()).hexdigest()[:16],
        "code_snippet": code_snippet[:500],  # Erste 500 Zeichen
        "metadata": metadata,
    }

    current_block.append(block_entry)

    # Wenn Block voll ist, füge ihn zur Blockchain hinzu
    if len(current_block) >= BLOCK_SIZE:
        block = {
            "index": len(blockchain),
            "timestamp": time.time(),
            "transactions": current_block.copy(),
            "previous_hash": blockchain[-1]["hash"] if blockchain else "0" * 64,
        }

        # Berechne Hash des Blocks
        block_string = json.dumps(block, sort_keys=True)
        block["hash"] = hashlib.sha256(block_string.encode()).hexdigest()

        blockchain.append(block)
        current_block = []

        print(f"🔗 Block #{block['index']} zur Blockchain hinzugefügt")
        save_blockchain()


def get_blockchain_summary():
    """Gibt eine Zusammenfassung der Blockchain zurück"""
    if not blockchain:
        return "Blockchain ist leer"

    total_actions = sum(len(block["transactions"]) for block in blockchain)
    latest_actions = []

    # Sammle die letzten 5 Aktionen
    for block in reversed(blockchain[-3:]):  # Letzte 3 Blöcke
        for tx in reversed(block["transactions"][-5:]):  # Letzte 5 Transaktionen
            latest_actions.append(f"{tx['action']}: {tx['code_hash']}")
            if len(latest_actions) >= 5:
                break
        if len(latest_actions) >= 5:
            break

    return f"Blockchain: {len(blockchain)} Blöcke, {total_actions} Aktionen\nLetzte: {', '.join(latest_actions)}"


# === Code-Verarbeitungs-Tools ===
def analyze_code_structure(code):
    """Analysiert die Struktur des Codes"""
    lines = code.split("\n")
    structure = {
        "total_lines": len(lines),
        "functions": [],
        "classes": [],
        "imports": [],
        "comments": [],
        "complexity": 0,
    }

    for i, line in enumerate(lines):
        line = line.strip()

        # Funktionen finden
        if line.startswith("def "):
            structure["functions"].append(
                {"line": i + 1, "name": line[4:].split("(")[0]}
            )

        # Klassen finden
        elif line.startswith("class "):
            structure["classes"].append(
                {"line": i + 1, "name": line[6:].split("(")[0].split(":")[0]}
            )

        # Imports finden
        elif line.startswith(("import ", "from ")):
            structure["imports"].append(line)

        # Kommentare finden
        elif line.startswith("#"):
            structure["comments"].append(line)

        # Komplexität schätzen
        if any(
            keyword in line for keyword in ["if ", "for ", "while ", "try:", "except"]
        ):
            structure["complexity"] += 1

    return structure


def extract_code_patterns(code):
    """Extrahiert Code-Patterns"""
    patterns = {
        "design_patterns": [],
        "anti_patterns": [],
        "best_practices": [],
        "security_issues": [],
    }

    lines = code.lower()

    # Design Patterns erkennen
    if "factory" in lines and "create" in lines:
        patterns["design_patterns"].append("Factory Pattern")
    if "singleton" in lines and "instance" in lines:
        patterns["design_patterns"].append("Singleton Pattern")
    if "observer" in lines and "notify" in lines:
        patterns["design_patterns"].append("Observer Pattern")

    # Anti-Patterns erkennen
    if "global " in lines and lines.count("global") > 3:
        patterns["anti_patterns"].append("Excessive Global Variables")
    if "except:" in lines or "except exception:" in lines:
        patterns["anti_patterns"].append("Bare Exception Handling")
    if "eval(" in lines or "exec(" in lines:
        patterns["anti_patterns"].append("Dangerous eval/exec Usage")

    # Best Practices prüfen
    if "def " in lines and "docstring" in lines:
        patterns["best_practices"].append("Docstrings vorhanden")
    if "type_hint" in lines or ": str" in lines or ": int" in lines:
        patterns["best_practices"].append("Type Hints verwendet")

    # Security Issues
    if "password" in lines and "plain" in lines:
        patterns["security_issues"].append("Plain Text Passwords")
    if "sql" in lines and "format" in lines:
        patterns["security_issues"].append("SQL Injection Risk")

    return patterns


def run_code_analysis(file_path):
    """Führt eine vollständige Code-Analyse durch"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        # Struktur analysieren
        structure = analyze_code_structure(code)

        # Patterns extrahieren
        patterns = extract_code_patterns(code)

        # Zur Blockchain hinzufügen
        add_to_blockchain(
            "code_analysis",
            code,
            {"file": file_path, "structure": structure, "patterns": patterns},
        )

        return {
            "structure": structure,
            "patterns": patterns,
            "summary": f"Datei: {os.path.basename(file_path)}\n"
            f"Zeilen: {structure['total_lines']}\n"
            f"Funktionen: {len(structure['functions'])}\n"
            f"Klassen: {len(structure['classes'])}\n"
            f"Komplexität: {structure['complexity']}",
        }

    except Exception as e:
        return {"error": str(e)}


# === LLM Initialisierung (Starcoder2 GGUF mit TensorRT) ===
def init_llm():
    global llm
    try:
        print("🔄 Lade Starcoder2 Modell mit TensorRT...")

        # TensorRT und CUDA Optimierungen
        import os

        os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # Erste GPU verwenden
        os.environ["CUDA_LAUNCH_BLOCKING"] = "1"  # Bessere Fehlerbehandlung

        # GGUF Modell mit llama-cpp-python
        from llama_cpp import Llama

        print("📦 Lade Starcoder2 GGUF Modell...")
        model = Llama(
            model_path=MODELLPFAD,
            n_ctx=8192,  # Erhöhte Kontext-Länge
            n_gpu_layers=-1,  # ALLE Layer auf GPU (-1 = alle)
            n_threads=12,  # Mehr CPU Threads
            verbose=False,
            use_mmap=True,  # Memory Mapping für bessere Performance
            use_mlock=False,  # Deaktiviere Memory Locking
            seed=42,  # Reproduzierbare Ergebnisse
            n_batch=512,  # Batch-Größe für GPU
            rope_scaling_type=0,  # Keine RoPE Scaling
            rope_freq_base=1000,  # Standard RoPE Frequenz
            rope_freq_scale=10,  # Standard RoPE Scale
        )

        # Wrapper für einfache Nutzung
        class LocalLLM:
            def __init__(self, model):
                self.model = model
                print("✅ Starcoder2 GGUF Modell geladen!")

                # Sichere Attribut-Abfrage
                try:
                    print(f"🔧 GPU-Layer: {model.n_gpu_layers}")
                except AttributeError:
                    print("🔧 GPU-Layer: Nicht verfügbar")

                try:
                    print(f"🔧 Batch-Größe: {model.n_batch}")
                except AttributeError:
                    print("🔧 Batch-Größe: Nicht verfügbar")

                # Zeige verfügbare Methoden
                print(
                    "🔧 Verfügbare Methoden: create_completion, create_chat_completion, embed, tokenize, detokenize"
                )

                # TensorRT Status prüfen
                try:
                    import tensorrt as trt

                    print(f"🔧 TensorRT Version: {trt.__version__}")
                except ImportError:
                    print("⚠️ TensorRT nicht verfügbar")

            def __call__(self, prompt, max_tokens=MAX_TOKENS, temperature=TEMPERATURE):
                try:
                    # Kürze den Prompt falls nötig
                    max_prompt_length = 6000  # Sicherheitspuffer
                    if len(prompt) > max_prompt_length:
                        prompt = prompt[:max_prompt_length] + "..."

                    # Starcoder2-spezifischer Prompt (kürzer)
                    formatted_prompt = f"""<|system|>
Du bist ein intelligenter Code-Assistent namens "Joshuel" mit Blockchain-Integration. 
Du kannst Code analysieren, verbessern und in die Blockchain eintragen.

<|user|>
{prompt}

<|assistant|>"""

                    # Generierung mit Starcoder2
                    response = self.model(
                        formatted_prompt,
                        max_tokens=min(max_tokens, 1024),  # Begrenze auf 1024
                        temperature=temperature,
                        stop=["<|user|>", "<|system|>", "<|end|>"],
                        echo=False,
                    )

                    # Extrahiere die Antwort
                    if "choices" in response and len(response["choices"]) > 0:
                        text = response["choices"][0]["text"].strip()
                        return {"choices": [{"text": text}]}
                    else:
                        return {"choices": [{"text": "❌ Keine Antwort vom Modell"}]}

                except Exception as e:
                    print(f"Fehler bei Modell-Generierung: {e}")
                    return {
                        "choices": [
                            {
                                "text": f"❌ Modell-Fehler: {str(e)}\n\n"
                                f"Versuche JosScript neu zu starten oder "
                                f"das Modell zu überprüfen."
                            }
                        ]
                    }

        llm = LocalLLM(model)
        agent_status.set("🟢 Starcoder2 + TensorRT + Blockchain geladen")
        print("✅ Starcoder2 mit TensorRT und Blockchain erfolgreich geladen!")

    except Exception as e:
        print(f"❌ Fehler beim Laden des Modells: {e}")
        agent_status.set("🔴 Modell-Fehler")
        messagebox.showerror("Fehler", f"Starcoder2 konnte nicht geladen werden:\n{e}")


# === Erweiterte Funktionen ===
def frage_modell(anweisung):
    """Optimierte Modell-Abfrage für StarCoder2 als Code-Generator"""
    if not llm:
        return "❌ Modell nicht geladen"

    # Erkenne den Typ der Anfrage
    anweisung_lower = anweisung.lower()

    # Code-Generierung
    if any(
        word in anweisung_lower
        for word in [
            "erstelle",
            "schreibe",
            "generiere",
            "mache",
            "bau",
            "erstelle eine",
            "schreibe eine",
        ]
    ):
        prompt = f"""Du bist StarCoder2, ein spezialisierter Code-Generator.

AUFGABE: {anweisung}

Generiere nur den Code. Verwende ```python für Code-Blöcke.
Erkläre kurz was der Code macht, aber fokussiere dich auf funktionierenden Code."""

    # Code-Verbesserung
    elif any(
        word in anweisung_lower
        for word in [
            "verbessere",
            "optimiere",
            "refactore",
            "bessere",
            "verbessere den",
        ]
    ):
        prompt = f"""Du bist StarCoder2, ein Code-Optimierer.

AUFGABE: {anweisung}

Analysiere den Code und verbessere ihn. Zeige:
1. Was verbessert wurde
2. Den verbesserten Code in ```python
3. Warum die Änderungen besser sind"""

    # Code-Analyse
    elif any(
        word in anweisung_lower
        for word in [
            "analysiere",
            "erkläre",
            "was macht",
            "wie funktioniert",
            "verstehe",
        ]
    ):
        prompt = f"""Du bist StarCoder2, ein Code-Analyst.

AUFGABE: {anweisung}

Analysiere den Code und erkläre:
1. Was der Code macht
2. Wie er funktioniert
3. Mögliche Probleme oder Verbesserungen
4. Best Practices"""

    # Bug-Fixing
    elif any(
        word in anweisung_lower
        for word in ["fehler", "bug", "problem", "funktioniert nicht", "kaputt"]
    ):
        prompt = f"""Du bist StarCoder2, ein Bug-Finder und -Fixer.

AUFGABE: {anweisung}

1. Identifiziere das Problem
2. Erkläre warum es passiert
3. Zeige den gefixten Code in ```python
4. Teste die Lösung"""

    # Neue Features
    elif any(
        word in anweisung_lower
        for word in ["erweitere", "füge hinzu", "neue funktion", "feature"]
    ):
        prompt = f"""Du bist StarCoder2, ein Feature-Entwickler.

AUFGABE: {anweisung}

1. Verstehe was gewünscht ist
2. Zeige den erweiterten Code in ```python
3. Erkläre die neuen Features
4. Stelle sicher dass es mit dem bestehenden Code kompatibel ist"""

    # Allgemeine Anfragen
    else:
        prompt = f"""Du bist StarCoder2, ein intelligenter Code-Assistent.

AUFGABE: {anweisung}

Antworte hilfreich und strukturiert. Wenn du Code generierst, verwende ```python.
Fokussiere dich auf praktische, funktionierende Lösungen."""

    try:
        antwort = llm(prompt, max_tokens=1024)
        text = antwort["choices"][0]["text"].strip()

        # Zur Blockchain hinzufügen
        add_to_blockchain(
            "ai_query",
            anweisung,
            {"response_length": len(text), "prompt_type": "optimized"},
        )

        return text
    except Exception as e:
        return f"❌ Fehler bei Modell-Abfrage: {e}"


def ai_antwort_in_editor_einfuegen(antwort):
    """Fügt AI-Antwort direkt in den Editor ein"""
    try:
        # SICHERHEIT: Warnung bei JosScript selbst, aber erlaube es mit Bestätigung
        if "agent_simple.py" in current_file_path.get():
            # Frage Benutzer um Bestätigung
            bestaetigung = messagebox.askyesno(
                "⚠️ SICHERHEITSWARNUNG",
                "Sie sind dabei, JosScript selbst zu überschreiben!\n\n"
                "Dies könnte das Programm beschädigen.\n\n"
                "Möchten Sie fortfahren?\n\n"
                "Empfehlung: Verwenden Sie '🔧 Verbessern' oder '🚀 Erweitern' für sichere Vorschläge.",
            )

            if not bestaetigung:
                return (
                    f"❌ Abgebrochen: JosScript wurde nicht überschrieben.\n\n{antwort}"
                )

        # Extrahiere Code aus der Antwort (zwischen ```python und ```)
        if "```python" in antwort and "```" in antwort:
            start = antwort.find("```python") + 9
            end = antwort.find("```", start)
            code = antwort[start:end].strip()

            # Sichere den aktuellen Code als Backup
            current_code = editor.get("1.0", tk.END).strip()

            # FRAGE BENUTZER: Was soll mit dem bestehenden Code passieren?
            choice = messagebox.askyesnocancel(
                "🤖 CODE EINFÜGEN",
                "Wie soll der AI-Code eingefügt werden?\n\n"
                "JA = Bestehenden Code ersetzen (mit Backup)\n"
                "NEIN = AI-Code am Ende hinzufügen\n"
                "ABBRECHEN = Nur anzeigen, nicht einfügen\n\n"
                "⚠️ Bei Ersetzung wird der alte Code als Backup gespeichert!",
            )

            if choice is None:  # Abbrechen
                return f"ℹ️ Code nur angezeigt, nicht eingefügt:\n\n{antwort}"

            elif choice:  # JA = Ersetzen mit Backup
                # Erstelle Backup des aktuellen Codes
                if current_code:
                    backup_filename = f"backup_{int(time.time())}.py"
                    try:
                        with open(backup_filename, "w", encoding="utf-8") as f:
                            f.write(
                                f"# BACKUP vom {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                            )
                            f.write(f"# Original Code vor AI-Ersetzung\n")
                            f.write("=" * 50 + "\n\n")
                            f.write(current_code)

                        # Zeige Backup-Info
                        backup_info = f"💾 Backup gespeichert: {backup_filename}"
                    except Exception as e:
                        backup_info = f"⚠️ Backup fehlgeschlagen: {e}"
                else:
                    backup_info = "ℹ️ Kein Code zum Sichern vorhanden"

                # Lösche aktuellen Inhalt und füge neuen Code ein
                editor.delete("1.0", tk.END)
                editor.insert("1.0", code)
                action_type = "replaced_with_backup"

            else:  # NEIN = Am Ende hinzufügen
                # Füge AI-Code am Ende hinzu
                if current_code:
                    # Füge Leerzeile hinzu wenn nötig
                    if not current_code.endswith("\n"):
                        editor.insert(tk.END, "\n\n")
                    else:
                        editor.insert(tk.END, "\n")

                # Füge AI-Code hinzu
                editor.insert(tk.END, code)
                action_type = "appended"
                backup_info = ""

            # Markiere den eingefügten Code farblich (grün für 3 Sekunden)
            editor.tag_configure("inserted", background="#4CAF50", foreground="white")

            if choice:  # Ersetzt
                editor.tag_add("inserted", "1.0", "end")
            else:  # Hinzugefügt
                # Finde die Position des hinzugefügten Codes
                lines = editor.get("1.0", tk.END).split("\n")
                start_line = len(lines) - len(code.split("\n"))
                editor.tag_add("inserted", f"{start_line}.0", "end")

            # Entferne Markierung nach 3 Sekunden
            def remove_highlight():
                editor.tag_remove("inserted", "1.0", "end")

            root.after(3000, remove_highlight)

            # Zur Blockchain hinzufügen
            add_to_blockchain(
                "ai_code_insert",
                code,
                {
                    "source": "ai_response",
                    "action_type": action_type,
                    "backup_created": choice and bool(current_code),
                },
            )

            # Erstelle Ergebnis-Nachricht
            result_msg = f"✅ Code wurde in den Editor eingefügt (grün markiert)!\n"
            result_msg += (
                f"Aktion: {'Ersetzt mit Backup' if choice else 'Hinzugefügt'}\n"
            )

            if choice and current_code:
                result_msg += f"{backup_info}\n"
                result_msg += f"💡 Tipp: Falls Sie den alten Code wieder brauchen, laden Sie {backup_filename}\n"

            result_msg += f"\n{antwort}"

            return result_msg
        else:
            return f"ℹ️ Kein Code-Block gefunden. Antwort nur angezeigt:\n\n{antwort}"

    except Exception as e:
        return f"❌ Fehler beim Einfügen: {e}\n\n{antwort}"


def starte_agent_mit_einfuegen():
    """Startet den AI-Agenten und fügt Antwort direkt in Editor ein"""
    anweisung = eingabe.get("1.0", tk.END).strip()

    if not anweisung:
        messagebox.showwarning("Hinweis", "Bitte eine Anweisung eingeben.")
        return

    ausgabe.insert(tk.END, f"🤖 AGENT (MIT EINFÜGEN): {anweisung}\n")
    ausgabe.see(tk.END)

    # Frage Modell
    antwort = frage_modell(anweisung)

    # Füge Antwort in Editor ein
    result = ai_antwort_in_editor_einfuegen(antwort)

    ausgabe.insert(tk.END, f"🧠 ERGEBNIS:\n{result}\n")
    ausgabe.see(tk.END)


def starte_agent():
    """Startet den AI-Agenten mit Blockchain-Integration"""
    anweisung = eingabe.get("1.0", tk.END).strip()

    if not anweisung:
        messagebox.showwarning("Hinweis", "Bitte eine Anweisung eingeben.")
        return

    ausgabe.insert(tk.END, f"🤖 AGENT (NUR ANZEIGEN): {anweisung}\n")
    ausgabe.see(tk.END)

    # Frage Modell
    antwort = frage_modell(anweisung)

    ausgabe.insert(tk.END, f"🧠 ANTWORT (nur rechts angezeigt):\n{antwort}\n")
    ausgabe.see(tk.END)


def code_analysieren():
    """Analysiert den aktuellen Code mit Blockchain-Integration"""
    if not current_file_path.get():
        messagebox.showwarning("Hinweis", "Keine Datei geöffnet.")
        return

    try:
        # Vollständige Code-Analyse
        analysis = run_code_analysis(current_file_path.get())

        if "error" in analysis:
            messagebox.showerror(
                "Fehler", f"Fehler bei Code-Analyse: {analysis['error']}"
            )
            return

        # Zeige Analyse-Ergebnisse
        ausgabe.insert(tk.END, f"\n🔍 CODE-ANALYSE (Blockchain):\n")
        ausgabe.insert(tk.END, f"{analysis['summary']}\n\n")

        # Patterns anzeigen
        patterns = analysis["patterns"]
        if patterns["design_patterns"]:
            ausgabe.insert(
                tk.END,
                f"🎯 Design Patterns: {', '.join(patterns['design_patterns'])}\n",
            )
        if patterns["anti_patterns"]:
            ausgabe.insert(
                tk.END, f"⚠️ Anti-Patterns: {', '.join(patterns['anti_patterns'])}\n"
            )
        if patterns["best_practices"]:
            ausgabe.insert(
                tk.END, f"✅ Best Practices: {', '.join(patterns['best_practices'])}\n"
            )
        if patterns["security_issues"]:
            ausgabe.insert(
                tk.END,
                f"🔒 Security Issues: {', '.join(patterns['security_issues'])}\n",
            )

        ausgabe.see(tk.END)

    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler bei Code-Analyse: {e}")


def blockchain_anzeigen():
    """Zeigt die Blockchain-Informationen an"""
    summary = get_blockchain_summary()
    ausgabe.insert(tk.END, f"\n🔗 BLOCKCHAIN STATUS:\n{summary}\n")
    ausgabe.see(tk.END)


def code_automatisch_verarbeiten():
    """Verarbeitet alle Python-Dateien im aktuellen Verzeichnis"""
    python_files = []

    # Finde alle Python-Dateien
    for file in os.listdir("."):
        if file.endswith(".py") and file != "agent_simple.py":
            python_files.append(file)

    if not python_files:
        messagebox.showinfo("Info", "Keine Python-Dateien gefunden.")
        return

    ausgabe.insert(tk.END, f"\n🔄 AUTOMATISCHE VERARBEITUNG:\n")
    ausgabe.insert(tk.END, f"Gefundene Dateien: {len(python_files)}\n")

    for file in python_files:
        try:
            analysis = run_code_analysis(file)
            if "error" not in analysis:
                ausgabe.insert(
                    tk.END,
                    f"✅ {file}: {analysis['structure']['total_lines']} Zeilen\n",
                )
            else:
                ausgabe.insert(tk.END, f"❌ {file}: Fehler\n")
        except Exception as e:
            ausgabe.insert(tk.END, f"❌ {file}: {e}\n")

    ausgabe.see(tk.END)


def lade_ordner():
    """Lädt alle Dateien aus einem Ordner und zeigt eine Dateiliste"""
    ordner_pfad = filedialog.askdirectory(title="Ordner auswählen")
    if not ordner_pfad:
        return

    try:
        # Sammle alle Dateien im Ordner
        dateien = []
        # StarCoder2 unterstützt viele Programmiersprachen und Dateitypen
        unterstuetzte_typen = [
            # Programmiersprachen
            ".py",
            ".java",
            ".cpp",
            ".c",
            ".h",
            ".hpp",
            ".js",
            ".ts",
            ".jsx",
            ".tsx",
            ".cs",
            ".rb",
            ".php",
            ".pl",
            ".r",
            ".swift",
            ".go",
            ".rs",
            ".kt",
            ".scala",
            ".hs",
            ".clj",
            ".erl",
            ".ex",
            ".lisp",
            ".ml",
            ".fs",
            ".d",
            ".pas",
            ".f",
            ".ada",
            ".jl",
            ".m",
            ".rkt",
            ".scm",
            ".cl",
            ".groovy",
            # Skriptsprachen
            ".sh",
            ".ps1",
            ".bat",
            ".cmd",
            ".vbs",
            ".pyw",
            # Konfigurationsdateien
            ".json",
            ".yaml",
            ".yml",
            ".toml",
            ".ini",
            ".cfg",
            ".conf",
            ".config",
            ".xml",
            ".csv",
            ".tsv",
            ".properties",
            ".env",
            ".gitignore",
            # Dokumentation
            ".md",
            ".txt",
            ".rst",
            ".adoc",
            ".tex",
            ".doc",
            ".docx",
            # Web
            ".html",
            ".htm",
            ".css",
            ".scss",
            ".sass",
            ".less",
            ".vue",
            ".svelte",
            # Datenbank
            ".sql",
            ".db",
            ".sqlite",
            ".sqlite3",
            # Build & Deployment
            ".dockerfile",
            ".makefile",
            ".mk",
            ".cmake",
            ".gradle",
            ".maven",
            ".pom",
            ".build",
            ".sln",
            ".vcxproj",
            ".csproj",
            ".xcodeproj",
            # Andere
            ".log",
            ".lock",
            ".lockfile",
            ".package",
            ".requirements",
            ".setup",
            ".manifest",
            ".license",
            ".readme",
            ".changelog",
            ".version",
        ]

        for root, dirs, files in os.walk(ordner_pfad):
            for file in files:
                if any(
                    file.lower().endswith(ext.lower()) for ext in unterstuetzte_typen
                ):
                    file_path = os.path.join(root, file)
                    try:
                        # Prüfe Dateigröße (max 1MB pro Datei)
                        file_size = os.path.getsize(file_path)
                        if file_size > 1024 * 1024:  # 1MB
                            continue

                        dateien.append(
                            {
                                "name": file,
                                "path": file_path,
                                "size": file_size,
                                "relative_path": os.path.relpath(
                                    file_path, ordner_pfad
                                ),
                            }
                        )
                    except Exception as e:
                        print(f"Fehler beim Lesen von {file}: {e}")

        if not dateien:
            messagebox.showinfo(
                "Info", "Keine unterstützten Dateien im Ordner gefunden."
            )
            return

        # Sortiere Dateien nach Größe (kleinste zuerst für bessere Übersicht)
        dateien.sort(key=lambda x: x["size"])

        # Erstelle Dateiliste für Auswahl
        datei_liste = []
        for i, file_info in enumerate(dateien, 1):
            size_kb = file_info["size"] / 1024
            if size_kb > 1024:
                size_str = f"{size_kb/1024:.1f} MB"
            else:
                size_str = f"{size_kb:.0f} KB"

            datei_liste.append(
                f"{i:3d}. {file_info['name']} ({size_str}) - {file_info['relative_path']}"
            )

        # Zeige Dateiliste in der Konsole
        ordner_name = os.path.basename(ordner_pfad) if ordner_pfad else "Unbekannt"
        ausgabe.insert(tk.END, f"📁 ORDNER GELADEN: {ordner_name}\n")
        ausgabe.insert(tk.END, f"📊 STATISTIK:\n")
        ausgabe.insert(tk.END, f"   • Dateien gefunden: {len(dateien)}\n")
        ausgabe.insert(tk.END, f"   • Pfad: {ordner_pfad}\n\n")

        ausgabe.insert(tk.END, f"📋 DATEILISTE:\n")
        for datei_eintrag in datei_liste:
            ausgabe.insert(tk.END, f"   {datei_eintrag}\n")

        ausgabe.insert(tk.END, f"\n💡 TIPPS:\n")
        ausgabe.insert(
            tk.END,
            f"   • Verwenden Sie '📁 Datei laden' um eine spezifische Datei zu laden\n",
        )
        ausgabe.insert(
            tk.END,
            f"   • ODER geben Sie eine AI-Anweisung ein, die sich auf die Dateien bezieht\n",
        )
        ausgabe.insert(
            tk.END, f"   • Die AI kann jetzt über alle Dateien im Ordner sprechen\n"
        )
        ausgabe.insert(
            tk.END,
            f"   • StarCoder2 unterstützt {len(unterstuetzte_typen)}+ Dateitypen\n\n",
        )

        # Speichere Ordner-Info für AI-Zugriff
        global current_folder_info
        current_folder_info = {
            "path": ordner_pfad,
            "name": ordner_name,
            "files": dateien,
            "loaded_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        }

        # Setze aktuellen Pfad auf Ordner
        current_file_path.set(f"FOLDER:{ordner_pfad}")
        root.title(f"Joshuel - Ordner: {ordner_name} ({len(dateien)} Dateien)")

        # Zur Blockchain hinzufügen
        add_to_blockchain(
            "folder_load",
            f"Ordner: {ordner_pfad}",
            {
                "file_count": len(dateien),
                "files": [f["name"] for f in dateien],
            },
        )

        ausgabe.see(tk.END)

    except Exception as e:
        # Spezielle Behandlung für urllib3 str.title() Bug
        if "str.title() takes no arguments" in str(e):
            messagebox.showerror(
                "Fehler",
                "Temporärer Fehler beim Laden des Ordners. Bitte versuchen Sie es erneut.",
            )
            print(f"Debug - urllib3 Bug umgangen: {e}")
        else:
            messagebox.showerror("Fehler", f"Fehler beim Laden des Ordners: {e}")
            print(f"Debug - Fehler Details: {type(e).__name__}: {e}")


def lade_datei_aus_ordner():
    """Lädt eine spezifische Datei aus dem geladenen Ordner"""
    if not hasattr(globals(), "current_folder_info") or not current_folder_info:
        messagebox.showwarning(
            "Hinweis", "Kein Ordner geladen. Bitte laden Sie zuerst einen Ordner."
        )
        return

    # Erstelle Dateiliste für Auswahl
    dateien = current_folder_info["files"]
    datei_namen = [
        f"{i+1}. {f['name']} ({f['relative_path']})" for i, f in enumerate(dateien)
    ]

    # Erstelle Auswahl-Dialog
    dialog = tk.Toplevel(root)
    dialog.title("Datei aus Ordner auswählen")
    dialog.geometry("600x400")
    dialog.transient(root)
    dialog.grab_set()

    # Liste mit Scrollbar
    list_frame = ttk.Frame(dialog)
    list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    listbox = tk.Listbox(list_frame, font=("Consolas", 10))
    scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=listbox.yview)
    listbox.configure(yscrollcommand=scrollbar.set)

    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Fülle Liste
    for datei_name in datei_namen:
        listbox.insert(tk.END, datei_name)

    selected_file = None

    def on_select():
        nonlocal selected_file
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            selected_file = dateien[index]
            dialog.destroy()

    def on_cancel():
        dialog.destroy()

    # Buttons
    button_frame = ttk.Frame(dialog)
    button_frame.pack(fill=tk.X, padx=10, pady=10)

    select_btn = tk.Button(
        button_frame,
        text="Datei laden",
        command=on_select,
        bg=COLORS["file"],
        fg="white",
    )
    select_btn.pack(side=tk.LEFT, padx=(0, 10))

    cancel_btn = tk.Button(button_frame, text="Abbrechen", command=on_cancel)
    cancel_btn.pack(side=tk.LEFT)

    # Doppelklick zum Laden
    listbox.bind("<Double-Button-1>", lambda e: on_select())

    # Warte auf Auswahl
    dialog.wait_window()

    # Lade ausgewählte Datei
    if selected_file:
        try:
            with open(selected_file["path"], "r", encoding="utf-8") as f:
                content = f.read()

            editor.delete("1.0", tk.END)
            editor.insert("1.0", content)
            current_file_path.set(selected_file["path"])

            root.title(
                f"Joshuel - {selected_file['name']} (aus {current_folder_info['name']})"
            )

            ausgabe.insert(tk.END, f"📄 DATEI GELADEN: {selected_file['name']}\n")
            ausgabe.insert(tk.END, f"   Pfad: {selected_file['relative_path']}\n")
            ausgabe.insert(tk.END, f"   Größe: {selected_file['size']} Bytes\n\n")
            ausgabe.see(tk.END)

        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Laden der Datei: {e}")


def lade_datei():
    """Lädt eine Datei"""
    pfad = filedialog.askopenfilename(
        filetypes=[("Python files", "*.py"), ("All files", "*.*")]
    )
    if pfad:
        try:
            with open(pfad, "r", encoding="utf-8") as f:
                inhalt = f.read()

            editor.delete("1.0", tk.END)
            editor.insert("1.0", inhalt)
            current_file_path.set(pfad)

            root.title(f"Joshuel - {os.path.basename(pfad)}")

        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Laden der Datei: {e}")


def lade_josscript():
    """Lädt automatisch JosScript selbst"""
    try:
        with open("agent_simple.py", "r", encoding="utf-8") as f:
            inhalt = f.read()

        editor.delete("1.0", tk.END)
        editor.insert("1.0", inhalt)
        current_file_path.set("agent_simple.py")

        root.title("Joshuel - agent_simple.py (SELF)")

        ausgabe.insert(tk.END, "🤖 JosScript hat sich selbst geladen!\n")
        ausgabe.insert(tk.END, "💡 Du kannst jetzt:\n")
        ausgabe.insert(tk.END, "   - Den Code analysieren lassen\n")
        ausgabe.insert(tk.END, "   - Verbesserungen vorschlagen lassen\n")
        ausgabe.insert(tk.END, "   - Neue Features hinzufügen lassen\n")
        ausgabe.insert(tk.END, "   - Blockchain-Integration nutzen\n")

    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Laden von JosScript: {e}")


def verbessere_josscript():
    """Verbessert JosScript automatisch mit Blockchain-Integration"""
    if not current_file_path.get():
        messagebox.showwarning("Hinweis", "Bitte lade zuerst eine Datei.")
        return

    try:
        # Verwende den Code aus dem Editor statt aus der Datei
        code = editor.get("1.0", tk.END).strip()

        if not code:
            messagebox.showwarning("Hinweis", "Kein Code im Editor vorhanden.")
            return

        anweisung = (
            f"Verbessere diesen Code. Mache ihn robuster, effizienter und benutzerfreundlicher. "
            f"Füge Fehlerbehandlung, Kommentare und Best Practices hinzu:\n\n"
            f"{code}"
        )
        antwort = frage_modell(anweisung)

        ausgabe.insert(tk.END, f"\n🔧 VERBESSERUNGSVORSCHLÄGE:\n{antwort}\n")
        ausgabe.see(tk.END)

    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler bei Verbesserung: {e}")


def erweitere_josscript():
    """Erweitert JosScript mit neuen Features und Blockchain"""
    if not current_file_path.get():
        messagebox.showwarning("Hinweis", "Bitte lade zuerst eine Datei.")
        return

    try:
        # Verwende den Code aus dem Editor statt aus der Datei
        code = editor.get("1.0", tk.END).strip()

        if not code:
            messagebox.showwarning("Hinweis", "Kein Code im Editor vorhanden.")
            return

        anweisung = (
            f"Erweitere diesen Code um neue Features. Füge mindestens2-3eue Funktionen hinzu, "
            f"die den Code nützlicher machen. Zeige den erweiterten Code in ```python Blöcken:\n\n"
            f"{code}"
        )
        antwort = frage_modell(anweisung)

        ausgabe.insert(tk.END, f"\n🚀 ERWEITERUNGSVORSCHLÄGE:\n{antwort}\n")
        ausgabe.see(tk.END)

    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler bei Erweiterung: {e}")


def speichere_datei():
    """Speichert die aktuelle Datei"""
    if not current_file_path.get():
        messagebox.showwarning("Hinweis", "Keine Datei geöffnet.")
        return

    try:
        inhalt = editor.get("1.0", tk.END)
        with open(current_file_path.get(), "w", encoding="utf-8") as f:
            f.write(inhalt)

        # Zur Blockchain hinzufügen
        add_to_blockchain("file_save", inhalt[:500], {"file": current_file_path.get()})

        messagebox.showinfo(
            "Erfolg", "Datei gespeichert und zur Blockchain hinzugefügt!"
        )

    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Speichern: {e}")


# === GUI Layout ===
def create_gui():
    # Hauptfenster mit PanedWindow (vertikal)
    main_paned = tk.PanedWindow(
        root, orient=tk.VERTICAL, sashrelief=tk.RAISED, bg="#2b2b2b"
    )
    main_paned.pack(fill=tk.BOTH, expand=True)

    # Oberes PanedWindow (horizontal): Editor links, AI/Buttons rechts
    top_paned = tk.PanedWindow(
        main_paned, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, bg="#2b2b2b"
    )
    main_paned.add(top_paned, stretch="always")

    # Linker Bereich: Editor + Datei-Operationen
    left_frame = ttk.Frame(top_paned)
    top_paned.add(left_frame, minsize=400, stretch="always")

    # === DATEI-OPERATIONEN (GRÜN) ===
    file_frame = ttk.Frame(left_frame)
    file_frame.pack(fill=tk.X, pady=(0, 10))

    file_label = tk.Label(
        file_frame,
        text="📁 DATEI-OPERATIONEN",
        bg=COLORS["file"],
        fg="white",
        font=("Arial", 10, "bold"),
    )
    file_label.pack(anchor=tk.W, pady=(0, 5))

    file_button_frame = ttk.Frame(file_frame)
    file_button_frame.pack(fill=tk.X)

    # Datei laden Button
    load_btn = tk.Button(
        file_button_frame,
        text="📁 Datei laden",
        bg=COLORS["file"],
        fg="white",
        font=("Arial", 9),
        command=lade_datei,
        relief=tk.FLAT,
        padx=10,
        pady=5,
    )
    load_btn.pack(side=tk.LEFT, padx=(0, 5))

    # Tooltip für Datei laden
    def show_load_tooltip(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
        label = tk.Label(
            tooltip,
            text="Lädt eine Python-Datei in den Editor",
            bg="yellow",
            fg="black",
            relief=tk.SOLID,
            borderwidth=1,
        )
        label.pack()
        load_btn.bind("<Leave>", lambda e: tooltip.destroy())

    load_btn.bind("<Enter>", show_load_tooltip)

    # JosScript laden Button
    self_btn = tk.Button(
        file_button_frame,
        text="🤖 JosScript laden",
        bg=COLORS["file"],
        fg="white",
        font=("Arial", 9),
        command=lade_josscript,
        relief=tk.FLAT,
        padx=10,
        pady=5,
    )
    self_btn.pack(side=tk.LEFT, padx=(0, 5))

    # Tooltip für JosScript laden
    def show_self_tooltip(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
        label = tk.Label(
            tooltip,
            text="Lädt JosScript selbst in den Editor",
            bg="yellow",
            fg="black",
            relief=tk.SOLID,
            borderwidth=1,
        )
        label.pack()
        self_btn.bind("<Leave>", lambda e: tooltip.destroy())

    self_btn.bind("<Enter>", show_self_tooltip)

    # Speichern Button
    save_btn = tk.Button(
        file_button_frame,
        text="💾 Speichern",
        bg=COLORS["file"],
        fg="white",
        font=("Arial", 9),
        command=speichere_datei,
        relief=tk.FLAT,
        padx=10,
        pady=5,
    )
    save_btn.pack(side=tk.LEFT, padx=(0, 5))

    # Tooltip für Speichern
    def show_save_tooltip(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
        label = tk.Label(
            tooltip,
            text="Speichert den Code und fügt ihn zur Blockchain hinzu",
            bg="yellow",
            fg="black",
            relief=tk.SOLID,
            borderwidth=1,
        )
        label.pack()
        save_btn.bind("<Leave>", lambda e: tooltip.destroy())

    save_btn.bind("<Enter>", show_save_tooltip)

    # Ordner laden Button
    folder_btn = tk.Button(
        file_button_frame,
        text="📁 Ordner laden",
        bg=COLORS["file"],
        fg="white",
        font=("Arial", 9),
        command=lade_ordner,
        relief=tk.FLAT,
        padx=10,
        pady=5,
    )
    folder_btn.pack(side=tk.LEFT, padx=(0, 5))

    # Tooltip für Ordner laden
    def show_folder_tooltip(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
        label = tk.Label(
            tooltip,
            text="Lädt alle unterstützten Dateien aus einem Ordner in den Editor",
            bg="yellow",
            fg="black",
            relief=tk.SOLID,
            borderwidth=1,
        )
        label.pack()
        folder_btn.bind("<Leave>", lambda e: tooltip.destroy())

    folder_btn.bind("<Enter>", show_folder_tooltip)

    # Datei aus Ordner laden Button
    load_from_folder_btn = tk.Button(
        file_button_frame,
        text="📁 Datei aus Ordner laden",
        bg=COLORS["file"],
        fg="white",
        font=("Arial", 9),
        command=lade_datei_aus_ordner,
        relief=tk.FLAT,
        padx=10,
        pady=5,
    )
    load_from_folder_btn.pack(side=tk.LEFT, padx=(0, 5))

    # Tooltip für Datei aus Ordner laden
    def show_load_from_folder_tooltip(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
        label = tk.Label(
            tooltip,
            text="Lädt eine spezifische Datei aus dem geladenen Ordner in den Editor",
            bg="yellow",
            fg="black",
            relief=tk.SOLID,
            borderwidth=1,
        )
        label.pack()
        load_from_folder_btn.bind("<Leave>", lambda e: tooltip.destroy())

    load_from_folder_btn.bind("<Enter>", show_load_from_folder_tooltip)

    # Editor
    editor_label = ttk.Label(left_frame, text="📝 Code Editor")
    editor_label.pack(anchor=tk.W)

    global editor
    editor = ScrolledText(
        left_frame, bg="#1e1e1e", fg="#ffffff", insertbackground="#ffffff", height=25
    )
    editor.pack(fill=tk.BOTH, expand=True)

    # Rechter Bereich: AI/Buttons/Analyse/Blockchain
    right_frame = ttk.Frame(top_paned)
    top_paned.add(right_frame, minsize=350, stretch="always")

    # Status
    status_label = ttk.Label(right_frame, textvariable=agent_status)
    status_label.pack(anchor=tk.W, pady=(0, 10))

    # Eingabe
    eingabe_label = ttk.Label(right_frame, text="🤖 AI-Anweisung")
    eingabe_label.pack(anchor=tk.W)

    global eingabe
    eingabe = ScrolledText(
        right_frame, bg="#1e1e1e", fg="#ffffff", insertbackground="#ffffff", height=8
    )
    eingabe.pack(fill=tk.X, pady=(0, 10))

    # === AI-FUNKTIONEN (BLAU) ===
    ai_frame = ttk.Frame(right_frame)
    ai_frame.pack(fill=tk.X, pady=(0, 10))

    ai_label = tk.Label(
        ai_frame,
        text="🤖 AI-FUNKTIONEN",
        bg=COLORS["ai"],
        fg="white",
        font=("Arial", 10, "bold"),
    )
    ai_label.pack(anchor=tk.W, pady=(0, 5))

    ai_button_frame = ttk.Frame(ai_frame)
    ai_button_frame.pack(fill=tk.X)

    # Agent starten (nur anzeigen)
    agent_btn = tk.Button(
        ai_button_frame,
        text="🚀 Agent starten",
        bg=COLORS["ai"],
        fg="white",
        font=("Arial", 9),
        command=starte_agent,
        relief=tk.FLAT,
        padx=10,
        pady=5,
    )
    agent_btn.pack(side=tk.LEFT, padx=(0, 5))

    # Tooltip für Agent starten
    def show_agent_tooltip(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
        label = tk.Label(
            tooltip,
            text="Startet AI-Agent - zeigt Antwort nur in der rechten Seite an\nCode wird NICHT in den Editor eingefügt",
            bg="yellow",
            fg="black",
            relief=tk.SOLID,
            borderwidth=1,
            justify=tk.LEFT,
        )
        label.pack()
        agent_btn.bind("<Leave>", lambda e: tooltip.destroy())

    agent_btn.bind("<Enter>", show_agent_tooltip)

    # Agent mit Einfügen (NEU!)
    agent_insert_btn = tk.Button(
        ai_button_frame,
        text="⚡ Code einfügen",
        bg=COLORS["ai"],
        fg="white",
        font=("Arial", 9),
        command=starte_agent_mit_einfuegen,
        relief=tk.FLAT,
        padx=10,
        pady=5,
    )
    agent_insert_btn.pack(side=tk.LEFT, padx=(0, 5))

    # Tooltip für Code einfügen
    def show_insert_tooltip(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
        label = tk.Label(
            tooltip,
            text="Startet AI-Agent und fügt Code direkt in den Editor ein\nCode wird grün markiert für 3 Sekunden\nÜberschreibt aktuellen Inhalt",
            bg="yellow",
            fg="black",
            relief=tk.SOLID,
            borderwidth=1,
            justify=tk.LEFT,
        )
        label.pack()
        agent_insert_btn.bind("<Leave>", lambda e: tooltip.destroy())

    agent_insert_btn.bind("<Enter>", show_insert_tooltip)

    # === CODE-ANALYSE (LILA) ===
    code_frame = ttk.Frame(right_frame)
    code_frame.pack(fill=tk.X, pady=(0, 10))

    code_label = tk.Label(
        code_frame,
        text="🔍 CODE-ANALYSE",
        bg=COLORS["code"],
        fg="white",
        font=("Arial", 10, "bold"),
    )
    code_label.pack(anchor=tk.W, pady=(0, 5))

    code_button_frame = ttk.Frame(code_frame)
    code_button_frame.pack(fill=tk.X)

    # Code analysieren
    analyze_btn = tk.Button(
        code_button_frame,
        text="🔍 Analysieren",
        bg=COLORS["code"],
        fg="white",
        font=("Arial", 9),
        command=code_analysieren,
        relief=tk.FLAT,
        padx=10,
        pady=5,
    )
    analyze_btn.pack(side=tk.LEFT, padx=(0, 5))

    # Tooltip für Code analysieren
    def show_analyze_tooltip(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
        label = tk.Label(
            tooltip,
            text="Analysiert den Code und zeigt Struktur, Patterns und Metriken\nVerwendet Blockchain für Verfolgung",
            bg="yellow",
            fg="black",
            relief=tk.SOLID,
            borderwidth=1,
            justify=tk.LEFT,
        )
        label.pack()
        analyze_btn.bind("<Leave>", lambda e: tooltip.destroy())

    analyze_btn.bind("<Enter>", show_analyze_tooltip)

    # Verbessern
    improve_btn = tk.Button(
        code_button_frame,
        text="🔧 Verbessern",
        bg=COLORS["code"],
        fg="white",
        font=("Arial", 9),
        command=verbessere_josscript,
        relief=tk.FLAT,
        padx=10,
        pady=5,
    )
    improve_btn.pack(side=tk.LEFT, padx=(0, 5))

    # Tooltip für Verbessern
    def show_improve_tooltip(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
        label = tk.Label(
            tooltip,
            text="Verbessert JosScript mit Vorschlägen\nSichere Methode - überschreibt nicht automatisch",
            bg="yellow",
            fg="black",
            relief=tk.SOLID,
            borderwidth=1,
            justify=tk.LEFT,
        )
        label.pack()
        improve_btn.bind("<Leave>", lambda e: tooltip.destroy())

    improve_btn.bind("<Enter>", show_improve_tooltip)

    # Erweitern
    extend_btn = tk.Button(
        code_button_frame,
        text="🚀 Erweitern",
        bg=COLORS["code"],
        fg="white",
        font=("Arial", 9),
        command=erweitere_josscript,
        relief=tk.FLAT,
        padx=10,
        pady=5,
    )
    extend_btn.pack(side=tk.LEFT, padx=(0, 5))

    # Tooltip für Erweitern
    def show_extend_tooltip(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
        label = tk.Label(
            tooltip,
            text="Erweitert JosScript um neue Features\nSichere Methode - überschreibt nicht automatisch",
            bg="yellow",
            fg="black",
            relief=tk.SOLID,
            borderwidth=1,
            justify=tk.LEFT,
        )
        label.pack()
        extend_btn.bind("<Leave>", lambda e: tooltip.destroy())

    extend_btn.bind("<Enter>", show_extend_tooltip)

    # === BLOCKCHAIN (ORANGE) ===
    blockchain_frame = ttk.Frame(right_frame)
    blockchain_frame.pack(fill=tk.X, pady=(0, 10))

    blockchain_label = tk.Label(
        blockchain_frame,
        text="🔗 BLOCKCHAIN",
        bg=COLORS["blockchain"],
        fg="white",
        font=("Arial", 10, "bold"),
    )
    blockchain_label.pack(anchor=tk.W, pady=(0, 5))

    blockchain_button_frame = ttk.Frame(blockchain_frame)
    blockchain_button_frame.pack(fill=tk.X)

    # Blockchain anzeigen
    bc_show_btn = tk.Button(
        blockchain_button_frame,
        text="📊 Blockchain Status",
        bg=COLORS["blockchain"],
        fg="white",
        font=("Arial", 9),
        command=blockchain_anzeigen,
        relief=tk.FLAT,
        padx=10,
        pady=5,
    )
    bc_show_btn.pack(side=tk.LEFT, padx=(0, 5))

    # Tooltip für Blockchain anzeigen
    def show_bc_tooltip(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
        label = tk.Label(
            tooltip,
            text="Zeigt Blockchain-Status und letzte Aktionen",
            bg="yellow",
            fg="black",
            relief=tk.SOLID,
            borderwidth=1,
        )
        label.pack()
        bc_show_btn.bind("<Leave>", lambda e: tooltip.destroy())

    bc_show_btn.bind("<Enter>", show_bc_tooltip)

    # Auto-Verarbeitung
    auto_btn = tk.Button(
        blockchain_button_frame,
        text="🔄 Auto-Verarbeitung",
        bg=COLORS["blockchain"],
        fg="white",
        font=("Arial", 9),
        command=code_automatisch_verarbeiten,
        relief=tk.FLAT,
        padx=10,
        pady=5,
    )
    auto_btn.pack(side=tk.LEFT, padx=(0, 5))

    # Tooltip für Auto-Verarbeitung
    def show_auto_tooltip(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
        label = tk.Label(
            tooltip,
            text="Analysiert automatisch alle Python-Dateien im Verzeichnis",
            bg="yellow",
            fg="black",
            relief=tk.SOLID,
            borderwidth=1,
        )
        label.pack()
        auto_btn.bind("<Leave>", lambda e: tooltip.destroy())

    auto_btn.bind("<Enter>", show_auto_tooltip)

    # UNTERER BEREICH: Konsole (AI-Ausgabe & Blockchain)
    console_frame = ttk.Frame(main_paned)
    main_paned.add(console_frame, minsize=120, stretch="always")

    console_label = ttk.Label(console_frame, text="🧠 AI-Ausgabe & Blockchain")
    console_label.pack(anchor=tk.W)

    global ausgabe
    ausgabe = ScrolledText(
        console_frame,
        bg="#1e1e1e",
        fg="#ffffff",
        insertbackground="#ffffff",
        height=15,
        font=("Consolas", 9),
    )
    ausgabe.pack(fill=tk.BOTH, expand=True)


# === Hauptfunktion ===
def init_app():
    """Initialisiert die Anwendung"""
    print("🚀 Starte JosScript mit Blockchain-Integration...")

    # Blockchain laden
    load_blockchain()

    # GUI erstellen
    create_gui()

    # LLM initialisieren
    init_llm()

    # Willkommensnachricht
    ausgabe.insert(tk.END, "🤖 Willkommen bei JosScript mit Blockchain!\n")
    ausgabe.insert(tk.END, "💡 Neue Features:\n")
    ausgabe.insert(tk.END, "   - 🔗 Blockchain-Integration\n")
    ausgabe.insert(tk.END, "   - 🔍 Erweiterte Code-Analyse\n")
    ausgabe.insert(tk.END, "   - 🎯 Pattern-Erkennung\n")
    ausgabe.insert(tk.END, "   - 🔄 Automatische Verarbeitung\n")
    ausgabe.insert(tk.END, "   - 📊 Code-Metriken\n")
    ausgabe.insert(tk.END, "   - ⚡ Direkte Code-Einfügung\n")
    ausgabe.insert(tk.END, "   - 🎨 Farbliche Kategorien\n")
    ausgabe.insert(tk.END, "   - 💬 Tooltips für alle Funktionen\n\n")

    ausgabe.insert(tk.END, "🎯 FARBKATEGORIEN:\n")
    ausgabe.insert(tk.END, "   🟢 GRÜN: Datei-Operationen (Laden, Speichern)\n")
    ausgabe.insert(tk.END, "   🔵 BLAU: AI-Funktionen (Agent, Code einfügen)\n")
    ausgabe.insert(
        tk.END, "   🟣 LILA: Code-Analyse (Analysieren, Verbessern, Erweitern)\n"
    )
    ausgabe.insert(tk.END, "   🟠 ORANGE: Blockchain (Status, Auto-Verarbeitung)\n\n")

    ausgabe.insert(tk.END, "📖 DETAILLIERTE ANLEITUNG:\n")
    ausgabe.insert(tk.END, "1️⃣ SCHRITT 1 - Code laden:\n")
    ausgabe.insert(
        tk.END, "   • Klicke '📁 Datei laden' (grün) um eine .py Datei zu laden\n"
    )
    ausgabe.insert(
        tk.END,
        "   • ODER klicke '📁 Ordner laden' um alle Dateien aus einem Ordner zu laden\n",
    )
    ausgabe.insert(
        tk.END, "   • ODER klicke '🤖 JosScript laden' um JosScript selbst zu laden\n"
    )
    ausgabe.insert(tk.END, "   • Der Code erscheint im Editor (linke Seite)\n\n")

    ausgabe.insert(tk.END, "2️⃣ SCHRITT 2 - AI verwenden:\n")
    ausgabe.insert(tk.END, "   • Schreibe eine ANWEISUNG in das AI-Eingabefeld\n")
    ausgabe.insert(tk.END, "   • StarCoder2 ist ein CODE-GENERATOR, kein Agent\n")
    ausgabe.insert(tk.END, "   • Sei SPEZIFISCH und DETAILLIERT in deiner Anfrage\n\n")

    ausgabe.insert(tk.END, "💡 BEISPIELE für gute Anfragen:\n")
    ausgabe.insert(
        tk.END, "   ✅ 'Erstelle eine Funktion die Fibonacci-Zahlen berechnet'\n"
    )
    ausgabe.insert(
        tk.END, "   ✅ 'Schreibe eine GUI mit tkinter für einen Taschenrechner'\n"
    )
    ausgabe.insert(
        tk.END, "   ✅ 'Verbessere diesen Code um ihn schneller zu machen'\n"
    )
    ausgabe.insert(tk.END, "   ✅ 'Füge eine Funktion hinzu die JSON-Dateien lädt'\n")
    ausgabe.insert(tk.END, "   ❌ 'Mache das besser' (zu vage)\n")
    ausgabe.insert(tk.END, "   ❌ 'Erstelle etwas' (zu unklar)\n\n")

    ausgabe.insert(tk.END, "🎯 STARCODER2 SPEZIALISIERUNG:\n")
    ausgabe.insert(tk.END, "   • Code-Generierung (erstelle, schreibe, generiere)\n")
    ausgabe.insert(
        tk.END, "   • Code-Verbesserung (verbessere, optimiere, refactore)\n"
    )
    ausgabe.insert(tk.END, "   • Code-Analyse (analysiere, erkläre, was macht)\n")
    ausgabe.insert(tk.END, "   • Bug-Fixing (fehler, problem, funktioniert nicht)\n")
    ausgabe.insert(
        tk.END, "   • Feature-Entwicklung (erweitere, füge hinzu, neue funktion)\n\n"
    )

    ausgabe.insert(
        tk.END, "⚠️ WICHTIG: Die AI kennt nur den Code der im Editor steht!\n"
    )
    ausgabe.insert(
        tk.END,
        "   Wenn Sie über eine Funktion sprechen, muss diese erst geladen werden.\n\n",
    )

    ausgabe.insert(tk.END, "🔒 SICHERHEIT:\n")
    ausgabe.insert(
        tk.END, "   • JosScript kann sich selbst überschreiben, aber mit Warnung\n"
    )
    ausgabe.insert(tk.END, "   • Sie werden vor dem Überschreiben gefragt\n")
    ausgabe.insert(
        tk.END,
        "   • Empfehlung: Verwenden Sie '🔧 Verbessern' oder '🚀 Erweitern' für sichere Vorschläge\n\n",
    )

    ausgabe.insert(
        tk.END,
        "⚡ NEUE FUNKTION: 'Code einfügen' - StarCoder kann jetzt direkt Code in den Editor einfügen!\n\n",
    )

    # Blockchain-Status anzeigen
    blockchain_anzeigen()

    # Starte GUI
    root.mainloop()


if __name__ == "__main__":
    init_app()
