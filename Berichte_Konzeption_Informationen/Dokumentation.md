# Speech Interaction - Mycroft Kalendar Skill
# (Benutzer)-Dokumentation
# Einleitung
Die Folgende Dokumentation beinhaltet die Anweisungen für die Installation eines Mycroft Skill und die Installation des Kalendar Skills. <br>
Desweiteren werden wichtige Methoden, Inputs und das Vorgehen erläutert.

## Aufgabenstellung
Das Ziel ist es einen Mycroft Skill selbständig auf einem Raspberri Pi zu erstellen. <br>
Es handelt sich hierbei um einen Kalender Manager Skill welcher sich mit einem Nextcloud Kalendar verbindet. <br>
Der Skill soll folgende Hauptfähigkeiten besitzen:
* Einen Terminen ausgeben
* Mehrere Termine aus einem Tag ausgeben
* Wenn kein Termin vorhanden ist, den nächstmöglichen Termin ausgeben
* Eine gezielte Anzahl an Termin ausgeben

Der Skill besitzt folgende Bonusfähigkeiten:
* Einen Termin anlegen
* Einen Termin umbennen
* Einen Termin löschen

Folgende Fähigkeiten sind zusätzlich eingbaut:
* Einen Kalender wechseln

Eine Konzeption der Aufgabenstellung kann in dem Ordner `Berichte_Konzeption_Information` unter folgenden Github [Link](https://github.com/dev-dot/calendar_manager_skill/tree/master/Berichte_Konzeption_Informationen) eingesehen werden.

# Grundsetzliche Mycroft Installation
Für diese Aufgabe wurde dementsprechend eine zur Verfügung gestellte Nextcloud und der Open-Source-Sprachassisten MyCroft verwendet. Zum Vorgehen wie man diesen auf dem RaspberryPi installiert findet man unter [**diesem Link**](https://mycroft-ai.gitbook.io/docs/using-mycroft-ai/get-mycroft/linux) eine Anleitung.


# Erstellen eines Mycroft Skills

Um einen Mycroft Skill zu erstellen kann mit Hilfe des `mycroft-msk create` Befehl, ein Template erstellt werden, welches anhand verschiedener Fragen einen Skill erstellt. Unteranderem wird nach dem Skillnamen und einem Beispiel Dialog gefragt, die der Benutzer vom Skill erwartet. Weitere Informationen und genauere Details können auf der offizielen Mycroft [**Seite**](https://mycroft-ai.gitbook.io/docs/skill-development/introduction/your-first-skill) nachgelesen werden.

Nach dem das Template erstellt wurde, wird der Skill automatisch auf der Githubseite veröffentlicht und auf dem Raspberry Pi installiert.

Alle installierten Skills befinden sich im Raspberry Pi im Verzeichnis `/opt/mycroft/skills`.

# Installation des `calendar_manager_skill`

## Voraussetzungen

Um den Calendar Manager Skill lauffähig zu installieren müssen bestimmte Vorraussetzungen erfüllt werden.

* Alle erforderlichen Packages müssen auf dem Raspberri Pi (falls nicht vorhanden) installiert werden. <br> Eine Liste der erfoderlichen Packages sind [**hier**](./packages_installed.md) mit den passenden befehlen zu finden.

* Ein Nextcloud Account muss vorhanden sein. <br> Für diesen Skill wurde ein Nextcloud Kalendar zur Verfügung gestellt. <br>
Den Kalendar kann unter folgendem [**Link**](https://si-nextcloud.social-robot.info/index.php/login) erreicht werden. <br>
Mit diesem Kalendar werden die Termine erstellt wie auch die ical-url generiert werden.

* Ein Account bei Mycroft wird benötigt um die Skills und Mycroft selbst zu konfigurieren. <br>
Die Mycroft Seite kann über [**Link**](https://account.mycroft.ai/) erreicht werden.

* Über den Skill Dashboard können alle installierten Skills eingesehen werden. <br>
Für den Calendar Manager Skill müssen die folgedenden erforderlichen Daten über die Webseite eingetragen werden: <br>
    * `Ical-Url` vom Nextcloud Kalender
    * `Username` des Nextcloud Accounts
    * `Password` des Nextcloud Accounts


## Installation
Um den den hier beschriebenen Calendar Manager Skill zu installieren gibt es zwei Möglichkeiten: <br>
* Möglichkeit 1: <br> Mithilfe des `mycroft-msm install <Github_Repo>` einen Skill installieren. <br>
In diesem Fall lautet der Befehl: `mycroft-msm install https://github.com/dev-dot/calendar_manager_skill.git` <br>
Der Skill wird dann im oben beschriebenen Verzeichnis installiert.

* Möglichkeit 2: <br>
Man muss in den  `/opt/mycroft/skills` Verzeichnis navigieren und den Skill mithilfe von Git clonen. `git clone https://github.com/dev-dot/calendar_manager_skill `

# Calendar Manager Skill

## Beschreibung
Der Calendar Manager Skill bietet verschiedene Befehle und Funktionen an um einen Termin aus dem Nextcloud Kalender abzufragen

## Helper Methoden

### `get_all_events()`
* Mit der Methode `get_all_events()` können wir, mit den Parametern `calendar`, optional `start` und `end`, die Kalendereinträge abrufen und die Methode gibt uns eine Liste mit allen gefundenen Events zurück.
Die Paramater geben den genutzten Kalender und einen Zeitraum an.

### `helper_speak_event()`
* Diese Methode hilft dabei die passenden Mycroft Dialoge auszugeben. Man übergibt ein Event, dass ausgegeben werden soll und die Methode überprüft anhand der Eventeigenschaften, ob es ein ganztägiges Event oder ein einstündiges Event ist und gibt dementsprechend den passenden Dialog aus.

### `get_ordinal_number()`
* Mit dieser Methode werden Zahlen für die englische Sprache ausgabefähig umgewandelt. Zum Beispiel aus 1 -> "first" und in der Aussgabe heißt es dann "first of july" statt "one of july".

## Intenthandler Methoden
Mit den Intenthandler Methoden kann der Benutzer nach bestimmten Aktionen fragen. Wenn der Benutzer den richtigen Input gibt, wird eine spezifische Methode ausgelöst und der Benutzer bekommt ein passende Aussage von Mycroft.

### `handle_next_appointment()`
* Wenn der Benutzer nach seinen zeitlich nächstmöglichen Termin fragt, wird sein nächster Termin ausgegeben. Falls kein Event in der Zukunft liegt, bekommt der Benutzer das auch mitgeteilt.<br>
Als Startzeitpunkt für die Suche wird der Moment der abfrage verwendet.

### `handle_ask_specific()`
* Mit dieser Methode kann der Benutzer nach einem Termin an einem bestimmten Datum fragen. Wenn an diesem Tag mehrere Termine vorhanden sind werden alle der Reihe nach vorgelesen.<br>
Existiert an dem Tag kein Termin teilt Mycroft das dem Benutzer mit und gibt zusätzlich den daraufhin nächsten Termin an welche beispielsweise ein Tag später wäre.
### `handle_ask_number()`
* Mit der `handle_ask_number()` Methode kann der Benutzer nach einer bestimmten Anzahl an Terminen frage. Der Benutzer gibt die gewünschte Anzahl mit und wenn genau so viele oder mehr Termine vorhanden sind, dann gibt Mycorft die exakt gewünschte Anzahl an Terminen aus.<br>
Sind weniger Termine wie angefragt vorhanden, teilt Mycroft dem Benutzer mit, dass beispielsweise nur vier anstatt der gewünschten Anzahl an Termine vorhanden sind und gibt diese daraufhin aus.
### `handle_choose_calendar())`
* Bei der `handle_choose_calendar())` Methode kann der Benutzer sein Kalender wechseln wenn er verschiedene Kalender in der Nextcloud hat. Alle Kalender werden als Auswahl vorgelesen und man kann per Spracheingabe seinen neuen Kalender wählen. Desweiteren besteht auch die Möglichkeit bei der Auswahl einen neuen Kalender zu erstellen.
### `handle_create_event()`
* Mit dieser Methode kann der Benutzer einen neuen Termin anlegen. Hierfür wird vom Benutzer ein `Name`, `Startdatum` und das `Enddatum` verlangt. Wenn der Benutzer einen ganztags Termin erstellen möchte, dann muss der Benutzer nach dem `Startdatum` noch `all day` sagen. Nachdem die Eingaben vollständig sind wird der Termin dem Kalender hinzugefügt. 

### `handle_delete_event()`
* Mit dieser Methode kann der Benutzer ein Termin löschen. <br>
Gibt der Benutzer keinen spezifisches Datum mit, fragt Mycroft nach dem Datum. Existiert nur ein Termin fragt Mycroft nochmal nach ob dieser Termin wirklich gelöscht werden soll, der Benutzer kann den Vorgang dann bestätigen oder abbrechen.<br>
Werden mehrere Termine an einen Tag gefunden, wird eine Liste erstellt und Mycroft liest diese vor. Anhand der ausgegebenen Position kann dann ein Event zum löschen ausgewählt werden. Der Ausgwählte Event muss dann vom Benutzer bestätigt werden.
Wurde das Event gelöscht bestätigt dies Mycroft.

### `handle_rename_event()`
* Mit dieser Methode kann der Benutzer ein Termin umbenennen. <br>
Gibt der Benutzer keinen spezifisches Datum mit, fragt Mycroft nach dem Datum. Existiert nur ein Termin fragt Mycroft nochmal nach ob dieser Termin wirklich umbennent werden soll, der Benutzer kann den Vorgang dann bestätigen oder abbrechen.<br>
Werden mehrere Termine an einen Tag gefunden, wird eine Liste erstellt und Mycroft liest diese vor. Anhand der ausgegebenen Position kann dann ein Event zum umbenennen ausgewählt werden.
<br> Sobald der Nutzer ein Termin zum umbennen ausgewählt hat, fragt Mycroft wie der Termin genannt werden soll und nimmt den Benutzer input.<br>
Wurder der Termin erfolgreich umbenannt und im Kalendar gespeichert, bestätigt dies Mycroft.



## wichtige Inputs / Befehle

### "What's my next appointment"
* Auf die Frage, beantwortet Mycroft die Frage mit dem nächstmöglich Termin im Kalender. Die Einträge werden chronologisch sortiert.
<br>
Beispiel:<br>
"Your next appointment will start on the fifteenth of June at 01:10 o'clock and will end on the   fifteenth of June at 02:10 o'clock and is entitled Dentist"

### "Do I have an appointment next {weekday}"
* Mycroft sucht nach dem Datum und gibt an wie viele Termine an diesem Tag im Kalender stehen und gibt diese auch direkt aus.
Für den Fall das an dem Tag kein Termin steht, sagt Mycroft das an dem Tag keine Termine vorhanden sind.
<br>
Beispiel <br>
"Yes, you have 2 appointments on wednesday the sixteenth of June. Your appointments are:
 Meeting with friends, starts at at 08:00 o'clock and will end at at 09:00 o'clock
 Dentist, starts at at 16:00 o'clock and will end at at 17:00 o'clock "

### "Tell me my next {Number} events"
* Mycroft sucht nach der bestimmten Anzahl an Terminen. Werden für die angefragten Anzahl an Terminen auch gleich viele gefunden gibt Mycroft diese aus.  <br>
Werden weniger Termine gefunden, gibt Mycroft die tatsächliche Nummer als Input an und gibt die gefundene Anzahl an Terminen aus. <br>
Werden keine Termine gefunden, da keine Termine mehr vorhanden sind, gibt Mycroft dies ebenfalls aus.

## Zusätzliche Methoden (Bonusaufgabe)
### "I want to create an appointment"
* 
### "I want to rename an appointment"
* 
### "I want to delete an appointment"
* 
# Wissenwertes während der Entwicklung (Title WIP)

Interessante Erkenntnisse und Probleme die während der Entwicklung zustande kamen, werden hier detailierter erläutert.


## Zwischenberichte während der Entwicklung

Innerhalb der Entwicklungszeit wurden zwei Zwischenberichte erstellt. Diese Zwischenberichte beschreiben,  die ersten Schritte wie auch Probleme, Besonderheiten und das weitere Vorgehen. <br>
Die Berichte befinden sich im Ordner `Berichte_Konzeption_Information` und können auch unter folgendem Github [Link](https://github.com/dev-dot/calendar_manager_skill/tree/master/Berichte_Konzeption_Informationen) gefunden werden

## Vorgehensweise
* 1. Nextcloud Verbindung herstellen
* 2. Caldav-Objekte verstehen und verarbeiten
* 3. Sortieren der Events nach Datum
* 4. Erstellen der Intents
* 5. Bonusaufgaben
* 6. Dokumentieren

## Probleme
 * Die Zeitzone festzulegen war eine große Herausforderung, da die Termine nicht mit der richtigen Uhrzeit wiedergegeben werden. <br>
 Gelöst wurde es mithilfe des Packages `tzlocal` und der Methode `get_localzone()`. Wir verwenden dementsprechend die Zeitzone des Raspberri Pi's. Dies bietet den Vorteil das die Zeitzone jederzeit vom Nutzer auf Wunsch auf seinem Gerät gewechselt werden kann.

* Die Credentials aus der Website wurden zu beginn nicht korrekt geladen. Sobald der Nutzer seine Daten auf der Webseite verändert hat, wurden die aktualisierten Daten nicht in die `settings.js` geschrieben, auch nicht bei einem Neustart des Geräts. <br>
Gelöst wurde es mit Hilfe einer Lifecyclemethode. Sobald neue Daten auf der Website für den Skill eingetragen werden, oder der Skill neugetartet wird, wird die `initialize` Methode aufgerufen. Diese führt eine Callbackmethode aus und schreibt wenn benötigt die aktualisierten Daten in die `settings.js`. Wenn alles korrekt ist wird die Verbindung zum Kalender bestätigt, falls nicht wird eine passende Fehlermeldung ausgegeben.
## Weiteres

## Pylint
