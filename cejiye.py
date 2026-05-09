#!/usr/bin/env python3
import subprocess
import json
import sys
import os
import datetime

CAS     = "\033[91m"
JALLE   = "\033[93m"
CAGAAR  = "\033[92m"
BULUUG  = "\033[94m"
DHAMAAN = "\033[0m"

ERRORS_DIR   = os.path.expanduser("~/cejiye-help/errors")
HISTORY_FILE = os.path.expanduser("~/cejiye-help/history.json")

def load_errors(filename):
    path = os.path.join(ERRORS_DIR, filename)
    with open(path) as f:
        return json.load(f)

def load_all_errors():
    git    = load_errors("git.json")
    python = load_errors("python.json")
    npm    = load_errors("npm.json")
    termux = load_errors("termux.json")
    return git + python + npm + termux

def find_error(text, errors):
    for error in errors:
        if error["pattern"].lower() in text.lower():
            return error
    return None

def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout + result.stderr

def show_list():
    files = ["git.json", "python.json", "npm.json", "termux.json"]
    for filename in files:
        errors = load_errors(filename)
        print(BULUUG + "\n📂 " + filename.replace(".json","").upper() + DHAMAAN)
        for i, e in enumerate(errors, 1):
            print(CAGAAR + f"  {i}. " + e["pattern"] + DHAMAAN)
            print(JALLE  + "     → " + e["cinwaan"] + DHAMAAN)

def add_error():
    print(BULUUG + "\n➕ Error Cusub Ku Dar" + DHAMAAN)
    files = ["git.json", "python.json", "npm.json", "termux.json"]
    print("\nNooca errors-ka:")
    for i, f in enumerate(files, 1):
        print(f"  {i}. {f.replace('.json', '')}")
    choice = input("\nNooca dooro (1-4): ")
    filename = files[int(choice) - 1]
    print(JALLE + "\nPattern-ka qor:" + DHAMAAN)
    pattern = input("> ")
    print(JALLE + "Cinwaanka Somali ah qor:" + DHAMAAN)
    cinwaan = input("> ")
    print(JALLE + "Sababta qor:" + DHAMAAN)
    sabab = input("> ")
    print(JALLE + "Xalka qor:" + DHAMAAN)
    xal = input("> ")
    path = os.path.join(ERRORS_DIR, filename)
    errors = load_errors(filename)
    errors.append({
        "pattern": pattern,
        "cinwaan": cinwaan,
        "sabab": sabab,
        "xal": xal
    })
    with open(path, "w") as f:
        json.dump(errors, f, indent=2, ensure_ascii=False)
    print(CAGAAR + "\n✅ Error si guul leh ayaa lagu daray!" + DHAMAAN)

def save_history(error, command):
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE) as f:
            history = json.load(f)
    else:
        history = []
    history.append({
        "taarikh": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "command": " ".join(command),
        "cinwaan": error["cinwaan"]
    })
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
def show_stats():
    if not os.path.exists(HISTORY_FILE):
        print(JALLE + "\nWali khalad ma dhicin!" + DHAMAAN)
        return
    with open(HISTORY_FILE) as f:
        history = json.load(f)
    counts = {}
    for h in history:
        cinwaan = h["cinwaan"]
        counts[cinwaan] = counts.get(cinwaan, 0) + 1
    sorted_errors = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    print(BULUUG + "\n📊 Errors-ka Ugu Badan" + DHAMAAN)
    for i, (cinwaan, count) in enumerate(sorted_errors, 1):
        print(CAGAAR + f"\n  {i}. {cinwaan}" + DHAMAAN)
        print(JALLE  + f"     Jeer: {count}" + DHAMAAN)
def show_history():
    if not os.path.exists(HISTORY_FILE):
        print(JALLE + "\nWali khalad ma dhicin!" + DHAMAAN)
        return
    with open(HISTORY_FILE) as f:
        history = json.load(f)
    print(BULUUG + "\n📜 Taariikhda Errors-ka" + DHAMAAN)
    for i, h in enumerate(history, 1):
        print(JALLE  + f"\n  {i}. {h['taarikh']}" + DHAMAAN)
        print(CAGAAR + f"     Command: {h['command']}" + DHAMAAN)
        print(CAS    + f"     Khalad:  {h['cinwaan']}" + DHAMAAN)

def main():
    if len(sys.argv) < 2:
        print("Isticmaalka: cejiye <command>")
        print("             cejiye list")
        print("             cejiye add")
        print("             cejiye history")
        return
    if sys.argv[1] == "list":
        show_list()
        return
    if sys.argv[1] == "add":
        add_error()
        return
    if sys.argv[1] == "history":
        show_history()
        return
    if sys.argv[1] == "stats":
        show_stats()
        return
    command = sys.argv[1:]
    output  = run_command(command)
    error   = find_error(output, load_all_errors())
    if error:
        save_history(error, command)
        print(CAS    + "\n⚠️  KHALAD: " + error["cinwaan"] + DHAMAAN)
        print(JALLE  + "📋 Sabab:   " + error["sabab"]    + DHAMAAN)
        print(CAGAAR + "✅ Xal:     " + error["xal"]      + DHAMAAN)
    else:
        print(output)

main()
