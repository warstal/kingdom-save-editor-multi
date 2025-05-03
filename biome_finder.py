import json
import sys

def find_biome_index(obj, path=""):
    """Rekursive Funktion, um alle Vorkommen von 'biomeIndex' zu finden"""
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "biomeIndex":
                print(f"Gefunden: {path}.{key} = {value}")
            else:
                find_biome_index(value, f"{path}.{key}")
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            find_biome_index(item, f"{path}[{i}]")

try:
    with open("global-v35.json", "r") as f:
        data = json.load(f)

    print("Suche nach biomeIndex...")
    find_biome_index(data)

    # Speziell für campaigns
    print("\nBiomeIndex für jede Kampagne:")
    for i, campaign in enumerate(data.get("campaigns", [])):
        # Prüfe direkt in der Kampagne
        if "biomeIndex" in campaign:
            print(f"Kampagne {i+1}: biomeIndex = {campaign['biomeIndex']}")
        # Suche in den Inseln
        if "_islands" in campaign:
            for j, island in enumerate(campaign["_islands"]):
                if "biomeIndex" in island:
                    print(f"  Kampagne {i+1}, Insel {j}: biomeIndex = {island['biomeIndex']}")
except Exception as e:
    print(f"Fehler: {e}")
