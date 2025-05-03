# Kingdom Two Crowns Save Editor

> **Hinweis:** Dieses Projekt basiert auf [bitwitch/kingdom-edit](https://github.com/bitwitch/kingdom-edit) und erweitert dessen Funktionen um eine benutzerfreundlichere Oberfläche und Norse Lands-Unterstützung.

Ein einfacher Savegame-Editor für Kingdom Two Crowns, mit dem verschiedene Aspekte des Spiels modifiziert werden können.

## Funktionen

- Zur Insel wechseln mit Geld und Crew
- Portale zerstören (alle oder nur nicht-Trigger Portale)
- Alle Feinde eliminieren
- Land auf maximales Level aufwerten
- Bäume zum Entfernen markieren
- Mit einer Gruppe an eine Position teleportieren
- Charaktere spawnen (Bogenschützen, Arbeiter, Pikenträger/Ritter)
- Münzen des Spielers bearbeiten

## Voraussetzungen & Nutzung

- Python 3.6 oder höher
- Nur Norse Lands und Call of Olympus werden derzeit unterstützt (andere DLCs und das Grundspiel aktuell nicht)
- Kopiere deine `global-v35` Datei aus dem Spielverzeichnis in den Ordner des Editors (z.B. `%AppData%\LocalLow\noio\KingdomTwoCrowns\Release`)
- Erstelle immer ein Backup deiner `global-v35` Datei, bevor du sie bearbeitest!
- starte die Kommandozeile (Eingabeaufforderung)
- wechsle mit `cd EDITORPFAD` in den Ordner des Editors
- Starte den Editor mit `python ktc_editor.py` und folge den Anweisungen
- Nach dem Bearbeiten die fertige Datei wieder zurück in den Release-Ordner kopieren

## Hinweise

- Die Kommandozeilennutzung ist ungetestet.
- Nur Spawning und Münzen editieren wurden getestet, die anderen Funktionen sind von bitwitch übernommen und ungetestet, stehen aber zur Verfügung.
- Einige komplexe Spielmechaniken könnten durch die Bearbeitung beeinträchtigt werden.

## Kommandozeilen-Nutzung (experimentell)

```bash
# Für Norse Lands
python kedit_norselands.py global-v35.json -i 0 edit_currency -p 0 -c 999

# Für Call of Olympus
python kedit.py global-v35.json -i 0 edit_currency -p 0 -c 999
```


Parameter:
- `-i, --island`: Index der Insel (meist 0)
- `-p, --player`: Spieler-Index (0 für Spieler 1, 1 für Spieler 2)
- `-c, --coins`: Anzahl der Münzen

## Weiterentwicklung

Dieses Projekt kann gerne von der Community weiterentwickelt werden. Mögliche Verbesserungen:

- Unterstützung für weitere DLCs
- Zusätzliche Bearbeitungsfunktionen
- Verbesserte Benutzeroberfläche
- Fehlerbehandlung und Stabilität

Die Nutzung erfolgt auf eigene Gefahr. Immer ein Backup der Spielstände anlegen!

Dieser Editor ist ein inoffizielles Tool und nicht mit den Entwicklern von Kingdom Two Crowns verbunden. Die Verwendung erfolgt auf eigene Gefahr. Es wird empfohlen, Backups deiner Spielstände zu erstellen, bevor du den Editor verwendest.

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz - siehe die LICENSE-Datei für Details.

## Ursprüngliches Projekt

Dieses Projekt ist eine Erweiterung von [bitwitch/kingdom-edit](https://github.com/bitwitch/kingdom-edit), das ursprünglich als Problemlösung für korrupte Spielstände in Kingdom Two Crowns: Call of Olympus auf der Nintendo Switch entwickelt wurde. Das ursprüngliche Projekt bot bereits die grundlegenden Funktionen zur Bearbeitung von Spielständen, war jedoch auf Call of Olympus beschränkt und hatte keine Benutzeroberfläche.

Aus der ursprünglichen README von bitwitch:

> "Warning: This is quick and dirty code that I wrote to solve my problem. I don't have time nor energy to make it a nice polished thing that is easy to use, but I am still releasing it just in case it can help someone anyway."