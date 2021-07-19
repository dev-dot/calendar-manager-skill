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

Um den Kalender Skill lauffähig zu installieren müssen bestimmte Vorraussetzungen erfüllt werden. 

* Alle erforderlichen Packages müssen auf dem Raspberri Pi falls nicht vorhanden installiert werden. <br> Eine Liste der erfoderlichen Packages ist [**hier**](**Link der Packege liste einfügen**) mit den passenden befehlen zu finden. 

* Ein Nextcloud Account muss vorhanden sein. <br> Für diesen Skill wurde ein Nextcloud Kalendar zur Verfügung gestellt. 

## Installation 
Um den den hier beschriebenen Kalender Skill zu installieren gibt es zwei Möglichkeiten: <br>
* Möglichkeit 1: <br> Mithilfe des `mycroft-msm install <Github_Repo>` einen Skill installieren. <br>
In diesem Fall lautet der Befehl: `mycroft-msm install https://github.com/dev-dot/calendar-manager-skill` <br>
Der Skill wird dann im oben beschriebenen Verzeichnis installiert.

* Möglichkeit 2: <br>
Man muss in den  `/opt/mycroft/skills` Verzeichnis navigieren und den Skill mithilfe von Git clonen. `git clone https://github.com/dev-dot/calendar-manager-skill ` 

