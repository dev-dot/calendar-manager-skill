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
* Einen Kalender wechseln oder wenn gewünscht einen weiteren Kalender in Nextcloud hinzufügen.


Eine Konzeption der Aufgabenstellung kann in dem Ordner `Berichte_Konzeption_Information` unter folgenden Github [Link](./Konzeption_1.pdf) eingesehen werden.

# Grundsetzliche Mycroft Installation
Für diese Aufgabe wurde dementsprechend eine zur Verfügung gestellte Nextcloud und der Open-Source-Sprachassisten MyCroft verwendet. Zum Vorgehen wie man diesen auf dem RaspberryPi installiert findet man unter [**diesem Link**](https://mycroft-ai.gitbook.io/docs/using-mycroft-ai/get-mycroft/linux) eine Anleitung.


# Erstellen eines Mycroft Skills

Um einen Mycroft Skill zu erstellen kann mit Hilfe des `mycroft-msk create` Befehl, ein Template erstellt werden, welches anhand verschiedener Fragen einen Skill erstellt. Unteranderem wird nach dem Skillnamen und einem Beispiel Dialog gefragt, die der Benutzer vom Skill erwartet. Weitere Informationen und genauere Details können auf der offizielen Mycroft [**Seite**](https://mycroft-ai.gitbook.io/docs/skill-development/introduction/your-first-skill) nachgelesen werden.

Nach dem das Template erstellt wurde, wird der Skill automatisch auf der Githubseite veröffentlicht und auf dem Raspberry Pi installiert.

Alle installierten Skills befinden sich im Raspberry Pi im Verzeichnis `/opt/mycroft/skills`.

# Installation des `calendar_manager_skill`

## Voraussetzungen

Um den Calendar Manager Skill lauffähig zu installieren müssen bestimmte Vorraussetzungen erfüllt werden.

* Alle erforderlichen Packages müssen auf dem Raspberri Pi (falls nicht vorhanden) installiert werden. <br> Für den Fall das bei der Installation die Packages nicht installiert wurden können die Packages manuell installiert werden. <br>
Eine Liste der erfoderlichen Packages sind [**hier**](./packages_installed.md) mit den passenden befehlen zu finden.

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



# Beispiele für die Inputs und Outputs

## Kalender Ausgaben
### `What's my next appointment`
* Auf die Frage, beantwortet Mycroft die Frage mit dem nächstmöglich Termin im Kalender. Die Einträge werden chronologisch sortiert.
<br><br>
Beispiel:<br>
"Your next event is" <br>
"Speech Interaction will start on the twenty-third of July at 15:00 o'clock and will end at 16:00 o'clock."

### `Do I have any appointments next {weekday}`
* Mycroft sucht nach dem Datum und gibt an wie viele Termine an diesem Tag im Kalender stehen und gibt diese auch direkt aus.
Für den Fall das an dem Tag kein Termin steht, sagt Mycroft das an dem Tag keine Termine vorhanden sind. <br> <br>
**Beispiel** <br>
"Yes, you have 2 appointments on the monday, july twenty-sixth, twenty twenty one. Your appointments are:" <br>
"basketball will start on the twenty-sixth of July and is an all day event. <br>
rock ballad and will start on the twenty-sixth of July at 16:00 o'clock and will end on the twenty-seventh of July at 19:00 o'clock."

### `Tell me my next {Number} events`
* Mycroft sucht nach der bestimmten Anzahl an Terminen. Werden für die angefragten Anzahl an Terminen  gleich viele gefunden gibt Mycroft diese aus.  <br>
Werden weniger Termine gefunden, gibt Mycroft die tatsächliche Nummer als Input an und gibt die gefundene Anzahl an Terminen aus. <br><br>
Werden keine Termine gefunden, da keine Termine mehr vorhanden sind, gibt Mycroft dies ebenfalls aus.
<br>
**Beispiel** <br>
Frage nach drei Terminen.
"You have only 2 upcoming events and they are" <br>
"Meeting will start on the twenty-third of July at 15:00 o'clock and will end at 16:00 o'clock. <br>
basketball will start on the twenty-sixth of July and is an all day event."




## Termine Manipulieren (Bonusaufgabe)
### `I want to create an appointment`
* Mycroft fragt, falls nicht direkt mitgegeben, nach dem gewünschten Datum, Startzeit, Endzeit und Titel.<br> <br>
**Beispiel**<br>
"Please tell me the name of the event?" - meeting <br>
"What date and time does the event start?" - friday 2 p.m. <br>
"At what date and time ended the event?" - friday 5 p.m. <br>
"Succesfully created the event lesson"

### `I want to rename an appointment`
* Mycroft fragt, falls nicht gegeben, nach dem Datum, dann welches Event umbenannt wird und wie es genannt werden soll.
<br> <br>
**Beispiel**<br>
"Please tell me the date of the event you want to rename" - monday <br>
"Do you want to rename this appointment basketball?" - yes <br>
"How do you want to call it?" - tennis <br>
"Successfully renamed"

### `I want to delete an appointment`
* Mycroft fragt, falls nicht gegeben, nach dem Datum, dann welches Event gelöscht werden soll.
<br> <br>
**Beispiel**<br>
" >> Please tell me the date of the event" - monday <br>
" Do you want to delete this appointment tennis? " - yes <br>
"How do you want to call it?" - tennis <br>
"Successfully deleted"

## Kalender wechseln
* Mycroft kann wenn gewünscht den Kalendar wechseln oder einen neuen erstellen.
<br> <br>

**Beispiel** <br>
"Choose from one of the following calendars by saying the number" <br>
"one, Persönlich" <br>
"two, Speech Interaction" <br>
"three, Arbeit" <br>
"four, create a new calendar" <br> - four
"How do you want to call the calendar?"  sport <br>
"New calendar sport was created and selected"


# Wissenwertes während der Entwicklung (Title WIP)

Interessante Erkenntnisse und Probleme die während der Entwicklung zustande kamen, werden hier detailierter erläutert.


## Zwischenberichte während der Entwicklung

Innerhalb der Entwicklungszeit wurden zwei Zwischenberichte erstellt. Diese Zwischenberichte beschreiben,  die ersten Schritte wie auch Probleme, Besonderheiten und das weitere Vorgehen. <br>
Die Berichte befinden sich im Ordner `Berichte_Konzeption_Information` und können auch unter folgendem Github [Link](https://github.com/dev-dot/calendar_manager_skill/tree/master/Berichte_Konzeption_Informationen) gefunden werden

## Vorgehensweise
1. Nextcloud <br>
    * Zuerst haben wir eine Verbindung zum Nextcloud Kalender aufgebaut.
 2. CalDAV
    * Mithilfe des CalDAV Packages konnten wir auf unseren Kalender zugreifen und eine Liste an Event-Objekte erstellen.<br>
    Desweiteren haben wir uns mit CalDAV auseinandergesetzt um die Funktionalitäten des Packages für unseren Skill besser einsetzen zu können.
 3. Behandeln der Events
    * Es werden immer nur die gewünschte Menge an Events abgerufen und je nach Funktion behandelt.
        * Ausgeben
        * Umbenennen
        * Erstellen
        * Löschen
 4. Erstellen der Intents
    * Damit Mycroft auf die Intents zugreifen kann müssen Methoden vorher mit `@intent_file_handler()` deklariert werden. Im Ordner `locale/en-us` müssen dann die Textfiles (`.intent`) mit den Aufruf Befehl gepeichert werden.
    Dialoge die Mycorft ausgibt müssen mit `.dialog` erstellt werden um im selben Ordner hinterlegt.
 5. Bonusaufgaben
    * Nachdem die Hauptfunktionalitäten entwickelt waren, haben wir uns an die Bonusaufgaben gesetzt. Zuerst haben wir die Zusatzfunktion `erstellen eines Termins ` programmiert und danach die restlichen beiden Skills `löschen und umbenennen`
 6. Weitere Zusatzfunktionen
    * Als weitere Zusatzfunktion bietet unser Skill dem Benutzer die Möglichkeit seinen Kalender in seiner
 Nextcloud zu wechseln und wenn gewünscht einen weiteren Kalender zu erstellen.
 7. Dokumention
    * Während der Entwicklung haben wir uns an die vorher dokumentierten Konzeption gehalten und wenn nötig leicht angepasst. Die Grundvoraussetzungen sind weiterhin gegeben.<br>
    Jedes Package welches wir verwenden haben wir zeitnah direkt dokumentiert um einen Überblick zu behalten.
    <br>
    Code Dokumentation wurden mit Docstrings durchgeführt.

## Probleme
 * Die Zeitzone festzulegen war eine große Herausforderung, da die Termine nicht mit der richtigen Uhrzeit wiedergegeben werden. <br>
 Gelöst wurde es mithilfe des Packages `tzlocal` und der Methode `get_localzone()`. Wir verwenden dementsprechend die Zeitzone des Raspberri Pi's. Dies bietet den Vorteil das die Zeitzone jederzeit vom Nutzer auf Wunsch auf seinem Gerät gewechselt werden kann.

* Die Credentials aus der Website wurden zu beginn nicht korrekt geladen. Sobald der Nutzer seine Daten auf der Webseite verändert hat, wurden die aktualisierten Daten nicht in die `settings.js` geschrieben, auch nicht bei einem Neustart des Geräts. <br>
Gelöst wurde es mit Hilfe einer Lifecyclemethode. Sobald neue Daten auf der Website für den Skill eingetragen werden, oder der Skill neugetartet wird, wird die `initialize` Methode aufgerufen. Diese führt eine Callbackmethode aus und schreibt wenn benötigt die aktualisierten Daten in die `settings.js`. Wenn alles korrekt ist wird die Verbindung zum Kalender bestätigt, falls nicht wird eine passende Fehlermeldung ausgegeben.


## Weiteres

## Pylint

Zum überprüfen unseres Codes haben wir `pylint` verwendet. Pylint dient dazu Fehler im Code anzuzeigen. Leider funktioniert pylint nicht perfekt mit Mycroft, weshalb wir manche Warnungen und Anmerkungen von Pylint deaktiviert haben. Der Grund dafür ist das Mycroft anders auf Funktionen und Zeilen zugreift.
<br>
Um Pylint auszufühen kann man in den Skill Ordner navigieren und `pylint __init__.py` ausführen.

<img src="./Pylint_Screenshot_Score_22072021.png"/>

[Pylint Score from the final commit - run on the Raspberry Pi running mycroft](./Pylint_Screenshot_Score_22072021.png)