# Zwischenbericht

## Erste Schritte
Auf unserem Pi:
* Pip3 upgraden und danach installierten wir msk mit dem Befehl pip3 install msk
* Skill erstellt mit Hilfe des Templates.
* Es war nicht Möglich den Skill auf das persönliche GitHub zu pushen, deshalb haben wir uns vom Template ein Repro erstellen lassen.

## Weitere Erfahrungen 
* Nextcloud Anbindung 
    * Anhand der verlinkten Caldav Dokumentation 
* Neues Repo 
* Probleme mit Caldav installation auf dem RasperryPi
    * `sudo apt-get install libxml2-dev libxslt-dev python-dev` wird benötigt für die Installion von libxml2 
    * Danach konnte `pip3 install caldav` ausgeführt werden.
* Danach konnte der Skill ohne Fehler (Modul import error) geladen werden. 
* Der Title vom Termin kann aus dem Terminkalender abegrufen und von Mycroft ausgegeben werden.

[**<- Zurück zur Dokumentation**](./Dokumentation.md)

