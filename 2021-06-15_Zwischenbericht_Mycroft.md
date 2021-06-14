# Zwischenbericht 15.06.2021

## Vollständige Funktionen
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

## Credentials
* Username / Password / CALDav-Link werden auf der Mycroft Skill Seite angegeben.

## Weitere Funktionen in Planungung
 ### "Tell me my next {three} appointments?"
 ### Bonusaufgaben
 ### Inputvalidierung

## Besonderheiten
* Einstellung der Zeitzone
* Wochentage werden als ints 0-6 gepeichert
* Datum wird im Dialog als Wort ausgesprochen und nicht als Zahl