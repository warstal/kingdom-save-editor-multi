@echo off

if "%~1" == "" (
    echo Sie müssen einen Dateinamen für die JSON-Ausgabe angeben
    exit /b 1
)

if not exist global-v35 (
    echo Keine Speicherdatei mit dem Namen "global-v35" gefunden
    exit /b 1
)

copy global-v35 tmp.gz
"C:\Program Files\7-Zip\7z.exe" e -y tmp.gz
type tmp | python -m json.tool > %1
del tmp.gz tmp

echo JSON-Datei erfolgreich erstellt: %1