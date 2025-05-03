import os
import json
import subprocess
import sys
import importlib.util
import argparse

def clear_screen():
    """Bildschirm löschen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def check_module(module_name):
    """Überprüft, ob ein Modul vorhanden ist"""
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        print(f"Fehler: Das Modul '{module_name}' wurde nicht gefunden!")
        print(f"Bitte stellen Sie sicher, dass die Datei '{module_name}.py' im gleichen Verzeichnis liegt.")
        return False
    return True

def check_batch_files():
    """Überprüft, ob die Batch-Dateien vorhanden sind"""
    if not os.path.exists("generate_json.bat"):
        print("Fehler: Die Datei 'generate_json.bat' wurde nicht gefunden!")
        return False
    if not os.path.exists("generate_save.bat"):
        print("Fehler: Die Datei 'generate_save.bat' wurde nicht gefunden!")
        return False
    return True

def generate_json():
    """Erstellt JSON-Datei aus global-v35"""
    print("Erstelle JSON-Datei aus global-v35...")
    json_filename = "global-v35.json"
    try:
        subprocess.run(["cmd", "/c", f"generate_json.bat {json_filename}"], shell=True)
        if os.path.exists(json_filename):
            return json_filename
        else:
            print(f"Fehler: Die Datei {json_filename} wurde nicht erstellt!")
            return None
    except Exception as e:
        print(f"Fehler beim Erstellen der JSON-Datei: {e}")
        return None

def generate_save(json_filename):
    """Erstellt global-v35 aus JSON-Datei"""
    print(f"Erstelle global-v35 aus {json_filename}...")
    try:
        subprocess.run(["cmd", "/c", f"generate_save.bat {json_filename}"], shell=True)
        if os.path.exists("global-v35"):
            print("Fertig! Die Datei global-v35 wurde erstellt.")
            return True
        else:
            print("Fehler: Die Datei global-v35 wurde nicht erstellt!")
            return False
    except Exception as e:
        print(f"Fehler beim Erstellen von global-v35: {e}")
        return False

def parse_json_file(filepath):
    """JSON-Datei laden"""
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Fehler beim Laden der JSON-Datei: {e}")
        return None

def save_json_file(data, filepath):
    """JSON-Datei speichern"""
    try:
        with open(filepath, "w") as f:
            json.dump(data, f)
        print(f"Änderungen wurden in {filepath} gespeichert.")
        return True
    except Exception as e:
        print(f"Fehler beim Speichern der JSON-Datei: {e}")
        return False

def get_biome_name(biome_index):
    """Gibt den Namen des Bioms zurück"""
    biome_names = {
        3: "Norse Lands",
        5: "Call of Olympus"
    }
    return biome_names.get(biome_index, f"Unbekannt ({biome_index})")

def get_biome_index(campaign):
    """Extrahiert den biomeIndex aus dem Campaign-Objekt"""
    # Durchsuche den gesamten Campaign-Eintrag nach biomeIndex
    if "biomeIndex" in campaign:
        return campaign["biomeIndex"]

    # Durchsuche auch in islands
    if "_islands" in campaign:
        for island in campaign["_islands"]:
            if "biomeIndex" in island:
                return island["biomeIndex"]

    # Wenn nichts gefunden wurde, geben 0 zurück
    return 0

def main_menu():
    """Hauptmenü anzeigen"""
    clear_screen()
    print("Kingdom Two Crowns Savegame Editor")
    print("==================================")

    # Schritt 1: global-v35 Datei überprüfen
    if not os.path.exists("global-v35"):
        print("Fehler: Die Datei 'global-v35' wurde nicht gefunden!")
        print("Bitte kopieren Sie die Datei aus:")
        print(r"%AppData%\LocalLow\noio\KingdomTwoCrowns\Release")
        input("Drücken Sie eine Taste, um das Programm zu beenden...")
        return

    # Nutzer fragen, ob fortgefahren werden soll
    print("\nDie Datei 'global-v35' wurde gefunden.")
    proceed = input("Fortfahren und JSON-Datei erstellen? (j/n): ").lower()
    if proceed != 'j':
        return

    # JSON-Datei erstellen
    json_filename = generate_json()
    if not json_filename or not os.path.exists(json_filename):
        print("Fehler: Konnte keine JSON-Datei erstellen!")
        input("Drücken Sie eine Taste, um das Programm zu beenden...")
        return

    # JSON-Datei laden
    data = parse_json_file(json_filename)
    if not data:
        input("Drücken Sie eine Taste, um das Programm zu beenden...")
        return

    # Schritt 2: Savegames auflisten
    while True:
        clear_screen()
        print("Verfügbare Spielstände:")
        print("======================")

        campaigns = data.get("campaigns", [])
        for i, campaign in enumerate(campaigns):
            # Biome-Index extrahieren
            biome_index = get_biome_index(campaign)
            biome_name = get_biome_name(biome_index)
            print(f"{i+1}. {biome_name}")

        print("\n0. Beenden")

        # Spielstand auswählen
        selected = -1
        while True:
            try:
                selected = int(input("\nWählen Sie einen Spielstand (0-{}): ".format(len(campaigns))))
                if 0 <= selected <= len(campaigns):
                    break
                else:
                    print("Ungültige Auswahl! Bitte wählen Sie eine Zahl zwischen 0 und {}.".format(len(campaigns)))
            except ValueError:
                print("Bitte geben Sie eine Zahl ein!")

        if selected == 0:
            # Beenden
            break

        # Index ist 0-basiert in der Liste, aber der Nutzer gibt 1-basiert ein
        selected -= 1

        # Schritt 3: BiomeIndex überprüfen
        campaign = campaigns[selected]
        biome_index = get_biome_index(campaign)

        if biome_index == 5:
            # Call of Olympus
            mode = "olympus"
            print("\nSpielstand: Call of Olympus")
        elif biome_index == 3:
            # Norse Lands
            mode = "norselands"
            print("\nSpielstand: Norse Lands")
        else:
            print(f"\nFehler: Der Biome-Index {biome_index} wird nicht unterstützt!")
            print("Nur Call of Olympus (5) und Norse Lands (3) werden derzeit unterstützt.")
            input("Drücken Sie eine Taste, um das Programm zu beenden...")
            sys.exit(1)  # Programm beenden

        # Spielstand-Menü anzeigen
        campaign_menu(data, selected, mode, biome_index)

    input("\nDrücken Sie eine Taste, um das Programm zu beenden...")

def campaign_menu(data, campaign_index, mode, biome_index):
    """Menü für einen bestimmten Spielstand anzeigen"""
    campaign = data["campaigns"][campaign_index]

    while True:
        clear_screen()
        print(f"Spielstand: {get_biome_name(biome_index)}")
        print("======================")

        # Insel auswählen
        if "_islands" in campaign:
            print("\nVerfügbare Inseln:")
            for i in range(len(campaign["_islands"])):
                print(f"{i}. Insel {i}")

            print("\n9. Zurück zum Hauptmenü")

            island = -1
            while True:
                try:
                    island = int(input("\nWählen Sie eine Insel (0-{}, 9 für Zurück): ".format(len(campaign["_islands"])-1)))
                    if island == 9:
                        return
                    elif 0 <= island < len(campaign["_islands"]):
                        break
                    else:
                        print(f"Ungültige Auswahl! Bitte wählen Sie eine Zahl zwischen 0 und {len(campaign['_islands'])-1} oder 9 für Zurück.")
                except ValueError:
                    print("Bitte geben Sie eine Zahl ein!")
        else:
            island = 0

        # Aktionen-Menü anzeigen
        action_menu(data, campaign_index, island, mode, biome_index)

def action_menu(data, campaign_index, island, mode, biome_index):
    """Menü für Aktionen anzeigen"""
    while True:
        clear_screen()
        print(f"Spielstand: {get_biome_name(biome_index)}, Insel: {island}")
        print("======================")

        actions = [
            "goto (Zur Insel wechseln, mit Geld und Crew)",
            "take_over (Alle nicht-Trigger Portale zerstören)",
            "destroy (Alle Portale zerstören)",
            "exterminate (Alle Feinde töten)",
            "pimp (Land auf maximales Level aufwerten)",
            "trees (Alle Bäume zum Entfernen markieren)",
            "formation (Mit einer Gruppe an eine Position teleportieren)",
            "spawn (Charaktere spawnen)",
            "edit_currency (Münzen des Spielers bearbeiten)",
            "save (Änderungen in JSON-Datei speichern)",
            "save+repack (Änderungen speichern und ins Spiel integrieren)"
        ]

        print("\nVerfügbare Aktionen:")
        for i, action in enumerate(actions):
            print(f"{i+1}. {action}")

        print("\n0. Zurück")

        # Aktion auswählen
        action_idx = -1
        while True:
            try:
                action_idx = int(input("\nWählen Sie eine Aktion (0-{}): ".format(len(actions))))
                if 0 <= action_idx <= len(actions):
                    break
                else:
                    print("Ungültige Auswahl! Bitte wählen Sie eine Zahl zwischen 0 und {}.".format(len(actions)))
            except ValueError:
                print("Bitte geben Sie eine Zahl ein!")

        if action_idx == 0:
            # Zurück
            return

        # Index ist 1-basiert in der Liste, aber wir wollen 0-basiert
        action_idx -= 1

        # Aktion ausführen
        action = actions[action_idx].split(" ")[0]

        # Import des entsprechenden Moduls
        if mode == "olympus":
            import kedit as editor
        else:  # norselands
            import kedit_norselands as editor

        # Campaign-Index setzen
        editor.campaign_index = campaign_index

        if action == "goto":
            # Zur Insel wechseln
            editor.action_goto(data, island)

        elif action == "take_over":
            # Alle nicht-Trigger Portale zerstören
            editor.action_take_over(data, island)

        elif action == "destroy":
            # Alle Portale zerstören
            editor.action_destroy(data, island)

        elif action == "exterminate":
            # Alle Feinde töten
            editor.action_exterminate(data, island)

        elif action == "pimp":
            # Land auf maximales Level aufwerten
            editor.action_pimp(data, island)

        elif action == "trees":
            # Alle Bäume zum Entfernen markieren
            editor.action_trees(data, island)

        elif action == "formation":
            # Mit einer Gruppe an eine Position teleportieren
            try:
                x = int(input("X-Position eingeben: "))
                editor.action_formation(data, island, x)
            except ValueError:
                print("Fehler: Bitte geben Sie eine Zahl ein!")
                input("Drücken Sie eine Taste, um fortzufahren...")
                continue

        elif action == "spawn":
            # Charaktere spawnen
            try:
                archers = int(input("Anzahl Bogenschützen: "))
                workers = int(input("Anzahl Arbeiter: "))

                if mode == "olympus":
                    pikemen = int(input("Anzahl Pikenträger: "))
                    editor.action_spawn(data, island, archers, workers, pikemen)
                else:  # norselands
                    knights = int(input("Anzahl Ritter: "))
                    editor.action_spawn(data, island, archers, workers, knights)
            except ValueError:
                print("Fehler: Bitte geben Sie eine Zahl ein!")
                input("Drücken Sie eine Taste, um fortzufahren...")
                continue
                
        elif action == "edit_currency":
            # Münzen des Spielers bearbeiten
            try:
                player_index = int(input("Spieler (1 oder 2): ")) - 1
                if player_index < 0 or player_index > 1:
                    print("Fehler: Bitte geben Sie 1 oder 2 ein!")
                    input("Drücken Sie eine Taste, um fortzufahren...")
                    continue
                    
                amount = int(input("Anzahl der Münzen: "))
                editor.action_edit_currency(data, island, player_index, amount)
            except ValueError:
                print("Fehler: Bitte geben Sie eine Zahl ein!")
                input("Drücken Sie eine Taste, um fortzufahren...")
                continue

        elif action == "save":
            # Änderungen in JSON-Datei speichern
            output_file = f"{action}_{island}.json"
            if save_json_file(data, output_file):
                print(f"Änderungen wurden in {output_file} gespeichert.")

        elif action == "save+repack":
            # Änderungen in JSON-Datei speichern
            output_file = f"modified_global-v35.json"
            if save_json_file(data, output_file):
                # Fragen, ob die Änderungen ins Spiel integriert werden sollen
                repack = input("Möchten Sie die Änderungen ins Spiel integrieren? (j/n): ").lower()
                if repack == 'j':
                    generate_save(output_file)

        input("\nDrücken Sie eine Taste, um fortzufahren...")

if __name__ == "__main__":
    # Überprüfe, ob die erforderlichen Module vorhanden sind
    modules_ok = True
    if not check_module("kedit"):
        modules_ok = False
        print("Hinweis: Das Modul 'kedit.py' wird für Call of Olympus benötigt.")
    if not check_module("kedit_norselands"):
        modules_ok = False
        print("Hinweis: Das Modul 'kedit_norselands.py' wird für Norse Lands benötigt.")

    # Überprüfe, ob die Batch-Dateien vorhanden sind
    if not check_batch_files():
        modules_ok = False

    if not modules_ok:
        print("\nEs fehlen einige erforderliche Dateien. Das Programm kann möglicherweise nicht korrekt funktionieren.")
        proceed = input("Möchten Sie trotzdem fortfahren? (j/n): ").lower()
        if proceed != 'j':
            sys.exit(1)

    main_menu()
