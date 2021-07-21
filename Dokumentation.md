# Speech Interaction - Mycroft Kalendar Skill
# (Benutzer)-Dokumentation
# Einleitung 
Die Folgende Dokumentation beinhaltet die Anweisungen für die Installation eines Mycroft Skill und die Installation des Kalendar Skills. <br>
Desweiteren werden wichtige Methoden und wichtige Inputs erläutert. 



# Grundsetzliche Mycroft Installation 
Für diese Aufgabe wurde dementsprechend eine zur Verfügung gestellte Nextcloud und der Open-Source-Sprachassisten MyCroft verwendet. Zum Vorgehen wie man diesen auf dem RaspberryPi installiert findet man unter [**diesem Link**](https://mycroft-ai.gitbook.io/docs/using-mycroft-ai/get-mycroft/linux) eine Anleitung.


# Erstellen eines Mycroft Skills 

Um einen Mycroft Skill zu erstellen kann mit Hilfe des `mycroft-msk create` Befehl, ein Template erstellt werden, welches anhand verschiedener Fragen einen Skill erstellt. Unteranderem wird nach dem Skillnamen und einem Beispiel Dialog gefragt, die der User vom Skill erwartet. Weitere Informationen und genauere Details können auf der offizielen Mycroft [**Seite**](https://mycroft-ai.gitbook.io/docs/skill-development/introduction/your-first-skill) nachgelesen werden.

Nach dem das Template erstellt wurde, wird der Skill automatisch auf der Githubseite veröffentlicht und auf dem Raspberry Pi installiert. 

Alle installierten Skills befinden sich im Raspberry Pi im Verzeichnis `/opt/mycroft/skills`. 

# Installation des `Calendar-Manager-Skill`

## Voraussetzungen

Um den Calendar Manager Skill lauffähig zu installieren müssen bestimmte Vorraussetzungen erfüllt werden. 

* Alle erforderlichen Packages müssen auf dem Raspberri Pi (falls nicht vorhanden) installiert werden. <br> Eine Liste der erfoderlichen Packages sind [**hier**](**Link der Packege liste einfügen**) mit den passenden befehlen zu finden. 

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
In diesem Fall lautet der Befehl: `mycroft-msm install https://github.com/dev-dot/calendar-manager-skill` <br>
Der Skill wird dann im oben beschriebenen Verzeichnis installiert.

* Möglichkeit 2: <br>
Man muss in den  `/opt/mycroft/skills` Verzeichnis navigieren und den Skill mithilfe von Git clonen. `git clone https://github.com/dev-dot/calendar-manager-skill ` 

# Calendar Manager Skill

## Beschreibung 
Der Calendar Manager Skill bietet verschiedene Befehle und Funktionen an um einen Termin aus dem Nextcloud Kalender abzufragen 

## Methodenbeschreibung
asd <br>
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
asd <br>
# Wissenwertes während der Entwicklung (Title WIP)

Interessante Erkenntnisse und Probleme die während der Entwicklung zustande kamen, werden hier detailierter erläutert. 


## Zwischenberichte während der Entwicklung

Innerhalb der Entwicklungszeit wurden zwei Zwischenberichte erstellt. Diese Zwischenberichte erstellt, welche die ersten Schritte wie auch Probleme, Besonderheiten und das weitere Vorgehen beschreiben. <br>
Die Berichte befinden sich im Ordner `Berichte_Konzeption_Information` und können auch unter folgendem Github [Bericht](LINK) gefunden werden 

## Besondere Erkenntnisse

## Probleme

## Weiteres

## Screenshot Pylint