# Work Log

**Student Name:** 

Instructions: Fill out one log for each course day. Content to consider: Course Sessions + Assignment

## Template:

---

## 1. ✅ What did I accomplish?

_Reflect on the activities, exercises, and work you completed today._

**Guiding questions:**
- What topics or concepts did you work with?
- What exercises or projects did you complete?
- What tools or technologies did you use?
- What did you learn or practice?



---

## 2. 🚧 What challenges did I face?

_Describe any difficulties, obstacles, or confusing moments you encountered._

**Guiding questions:**
- What was difficult to understand?
- Where did you get stuck?
- What errors or problems did you face?
- What felt frustrating or confusing?




---

## 3. 💡 How did I overcome them?

_Explain how you overcame the challenges or what help you needed._

**Guiding questions:**
- What strategies did you try?
- Who or what helped you (instructor, classmates, documentation)?
- What did you learn from solving the problem?
- What questions do you still have?


---

## Week 1

### Day 1

#### 1. ✅ What did I accomplish?

Erste Berührungspunkte mit GitHub und dessen Nutzen (warum wird es benutzt und wie verwendet man es grob)
Kleine Wiederholungen von Grundlagen der Programmierung aus Semester 1 wie Funktionen schreiben


---

#### 2. 🚧 What challenges did I face?

Funktionen im Zusammenhang mit uv/Zur Übertragung werden minimal anders geschrieben als die normalen Funktionen
'f"' in Funktionen zu verwenden in Kombination mit {} war mir neu
Neue Funktionen/Variabeln kennenlernen ist am Anfang immer etwas verwirrend/braucht Zeit zu verinnerlichen welche Funktion etc. was beinhaltet/macht.


---

#### 3. 💡 How did I overcome them?

Eigene Anwendung zuhause mit Rechenbeispiel und ein bisschen durchprobiert mit alten Funktionen aus Semester 1 um wieder in die Thematik reinzufinden.
Präsentation von Martin angeschaut und probiert es Schritt für Schritt nachzuvollziehen.
Bei kleinen Fehlermeldungen AI dazugezogen, meistens reicht aber Template durchlesen, oft ist ein Schreib- bzw. Formfehler das Problem


---



### Day 2

#### 1. ✅ What did I accomplish?

Wiederholung von grundlegenden Python Kenntnisse wie Datentypen, Funktionen, Dictionaries und Listen - war alles noch ziemlich aktuell im Kopf, aber gut es aufzufrischen
Create Notes mit eigenen Parametern.
Kommunikation bzw Abhängigkeit mit dem Json-File - was passiert wenn ich etwas in VSCode ändere auf dem Server und andersrum.
Wie programmiere ich eigene Notes und rufe diese ab. Im Anschluss daran wie man seine Notes in Kategorien einteilt und ausschließlich diese Kategorie mit den festgelegten anderen Parametern (Title, datetime..) abruft.
Die Stats der Notes abfragen, indem ich erst die Anzahl der Notes durchzähle (if-schleife) und im Anschluss die Notes by_category ausgebe. So kann ich wenn ich verschiedene Notes für unterschiedliche Themen habe abfragen wieviele es pro Thema bzw. Category sind. Bestimmt kann man im späteren Verlauf noch weitaus mehr abfragen bzw. interessantere Datenabfragen machen.


---

#### 2. 🚧 What challenges did I face?

Überhaupt erstmal in das ganze Thema reinzukommen find ich ziemlich kompliziert da es viel aufeinmal ist. Gerade im Online Unterricht kommt man mitunter nur schwer mit, wenn man andauernd sein Bildschirm switchen muss, schnelle Korrekturen gemacht werden usw.

Ich hatte zu Beginn Probleme damit zu verstehen, wie die ganzen Zusammenhänge sind mit allen Schnittstellen, mit denen wir gerade arbeiten.

Kleinere Programmierfehler wie zB. das notes_db, _ = load_notes() in die Tasks zu übernehmen war, damit das Programm läuft
Terminal neu laden nach einer Ausführung war eine kleine Herausforderung, ich konnte da dann immer nicht drauf zugreifen. Str+C hat dann funktioniert um nach einer Änderung wieder uv run.. auszuführen

---

#### 3. 💡 How did I overcome them?

Ausprobieren mit eigenen Kategorien, schauen wie sich die Instanzen gegeneinander beeinflussen.
Code durchlesen und nach Funktionen/Variablen googeln die ich nicht kannte, um den Code vollumfänglich zu verstehen.
Wenn es mal überhaupt nicht lief, hab ich meinen Code Gemini gegeben und gefragt wo es happert und mir die Zusammenhänge zwischen der Aufgabe und meinem Code erklären lassen.

---

### Day 3

#### 1. ✅ What did I accomplish?

REST API Design Prinzipien kennengelernt – also warum man URLs so aufbaut wie man sie aufbau und was der Unterschied zwischen Path- und Query-Parametern ist.
Den bestehenden Note API Code von Tag 2 schrittweise erweitert um vollständiges CRUD – also nicht nur erstellen und lesen, sondern jetzt auch updaten und löschen. PUT ersetzt dabei immer die komplette Note, PATCH nur die Felder die man mitschickt, wie bei mir zB. der title.

Tags als neues Feld eingebaut – der Unterschied zu Category ist dass eine Note mehrere Tags haben kann aber nur eine Category. - > neue Möglichkeiten zu filtern/mehr Details einzubringen.

Task 1 – Filter für GET /notes getestet. Category, Suchbegriff und Tag einzeln und kombiniert ausprobiert in /docs. Hab mir dafür gezielt Testnotizen mit unterschiedlichen Kategorien und Tags erstellt um alle Kombinationen sinnvoll durchzutesten.

Task 2 – Statistik-Endpoint ausgebaut. Hab collections.Counter aus der Python Standardbibliothek dazugezogen – das war neu für mich. Counter zählt automatisch wie oft ein Wert vorkommt, was das Zählen von Kategorien und Tags deutlich kürzer macht als mit einer manuellen if-Schleife.

Task 3 – Zwei neue Ressourcen gebaut: /categories gibt alle einzigartigen Kategorien zurück, /categories/{category_name}/notes filtert die Notes nach Kategorie. Das Prinzip hab ich von den Tag-Endpoints aus der Stunde übernommen und auf Kategorien angewendet. Hab dabei set() verwendet weil ein Set automatisch Duplikate rausfiltert – dafür musste ich etwas recherchieren, weil mir der Unterschied zwischen set und list bzw. wann diese eher zur Anwendung kommen nicht klar war.

Task 4 – PUT und PATCH Endpoints eingebaut. Für PATCH ein neues Modell NoteUpdate geschrieben wo alle Felder Optional sind – also nicht mitgeschickt werden müssen.

Task 5 – Datumsfilter in GET /notes eingebaut. Zwei neue optionale Parameter created_after und created_before ergänzt. Die Filter lassen sich außerdem mit allen anderen bestehenden Filtern kombinieren. Etwas blöd daran war, dass ich heute neue Notizen erstellt hatte wegen eines Errors in meiner json Datei, deswegen konnte ich die Filterung nicht wirklich prüfen, da alle dasselbe Erstellungsdatum hatten.

Task 6- Alle bisher bestehenden Notizen in eine Datenbank überführt, und dafür den gesamten Code überarbeitet, sodass die JSON Logik verschwindet und die der DB einfließt.


---

#### 2. 🚧 What challenges did I face?

Wie gesagt war meine notes.json Datei zu Beginn beschädigt – es stand irgendwie doppelter JSON Inhalt drin was einen JSON decode error ausgelöst hat bei jedem POST Request. War schwer nachzuvollziehen woran es liegt weil der Fehler sehr kryptisch war.

In /docs beim Testen hab ich versucht mehrere Notes auf einmal ins Textfeld einzufügen, was nicht geht weil das Feld immer nur eine einzige Note erwartet. Hat dann immer 422 Fehler gegeben.
Die Reihenfolge der Endpoints im Code war mir nicht bewusst dass sie wichtig ist – /notes/stats muss zum Beispiel vor /notes/{note_id} stehen weil FastAPI sonst denkt "stats" ist eine ID.

Beim Erweitern von GET /notes für Task 5 hab ich den alten Code nicht gelöscht sondern den neuen einfach davor eingefügt. Dadurch war der alte Code ausgegraut weil er nach dem return stand und nie erreicht wird.

Optional in Task 4 war am Anfang verwirrend. Generell kommens sehr oft Befehle/Code vor die ich noch nie zuvor gesehen habe.

In Task 6 fand ich die komplette Dokumentation der einzelnen Schritte leider zu wenig beschrieben, was unnötig viel Zeit gefressen hat. Ich wusste oft nicht was ich genau machen soll und was der Code den ich reinkopieren soll bedeutet. Außerdem war es schwer nachzuvollziehen wo neuer Code genau hingehört, damit man nicht von Fehlermeldungen wie xy ist nicht definiert überhäuft wurde.
Zudem fand ich es schwierig zu wissen was ich mit meinen alten Notizen machen soll, die den vorherigen Code erklärt haben.


---

#### 3. 💡 How did I overcome them?

Die kaputte JSON Datei hab ich gefixt indem ich den Inhalt komplett gelöscht und durch ein leeres Array [] ersetzt habe. DAnn hab ich den Server neu gestartet und die Notes nochmal neu und diesemal einzeln in POST eingegeben.

Beim 422 Fehler durch mehrfache Notes hab ich verstanden dass man in /docs immer nur eine Note pro Execute eingibt und dann wartet bis die Antwort mit ID und Timestamp zurückkommt bevor man die nächste eingibt.
Die Reihenfolge der Endpoints hab ich durch Ausprobieren und nachfragen verstanden – FastAPI liest den Code von oben nach unten und nimmt den ersten Treffer, deswegen müssen spezifischere Endpoints immer vor den generischen mit {id} stehen.

Den ausgegrauten Code in Task 5 hab ich einfach komplett gelöscht, nachdem ich sicher war, dass mein neuer Code alle Anforderungen erfüllt.

Den Optional Typ und den is not None Check hab ich mir über einen Chatbot erklären lassen.
Danach bzw. generell hab ich den Code für mich entsprechend kommentiert, damit ich das einerseits nicht vergesse und andererseits auch andere nachvollziehen können was da genau passiert.

Für Task 6 war ich leider ziemlich sehr auf die Hilfe von LLMs angewiesen die mir den Code erklären und wo ich ihn einfügen muss. Nach ein paar Stunden konnte ich den Aufbau und warum man was macht dann doch relativ gut nachvollziehen.
Um zukünftig besser klarzukommen hab ich den gesamten Aufbau dann nochmal verändert und neu kommentiert, damit alles deutlich übersichtlicher für mich ist.
Ich denke für die zukünftige Abarbeitung von Hausaufgaben ist es auch sinnvoll sich erstmal alle einzelnen Steps anzuschauen und zu verstehen um die spätere Integration im Code sinnvoller zu gestalten bzw. sich im Kopf schon mal Verknüpfungen zu machen wo welcher Codeblock Sinn macht einzufügen.




---

## Week 2

### Day 4

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

### Day 5

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

### Day 6

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

## Week 3

### Day 7

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

### Day 8

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

### Day 9

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---


# 🎉 Congratulations! You did it! 🎓✨













