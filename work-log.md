# Work Log

**Student Name: Elias Knoch**

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

Heute habe ich REST API Design Prinzipien kennengelernt, sprich warum man URLs so aufbaut wie man sie aufbaut und was der Unterschied zwischen Path- und Query-Parametern ist.
Den bestehenden Note API Code von Tag 2 schrittweise erweitert um vollständiges CRUD. Also nicht nur erstellen und lesen, sondern jetzt auch updaten und löschen. PUT ersetzt dabei immer die komplette Note, PATCH nur die Felder die man mitschickt, wie bei mir zB. der title.

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


Heute habe ich hauptsächlich gelernt wie der Code für Tests aufgebaut ist, und wie man Tests für ein bestehendes Programm schreibt, um zu prüfen wie gut es gegen Dinge wie Grenzfälle/falsche Angaben des Nutzers etc. abgesichert ist. 

Für unsere Anwendungsfälle waren die Libraries pytest,requests und faker wichtig, deren Funktionen ich durch das testen/anwenden verstehen konnte. Zudem konnte ich durch das testen die Statuscodes 200,201,404 und 422 noch einmal verinnerlichen. Darüber hinaus habe ich etwas error handling dazu gelernt durch die aufgetretenen Fehlermeldungen sowie das arbeiten im Terminal (in einem läuft der Server, in einem zweiten lässt man die Tests durchlaufen)


---

#### 2. 🚧 What challenges did I face?

Der schwierigste Teil war definitiv erstmal die Beispieltests bzw. den Code zu verstehen, da Code wie assert, oder requests noch neu für mich waren. 

Auch das Zusammenspiel zwischen dem laufenden Server, der Testdatei und dem Terminal waren zuerst einmal unklar. So kam es Beispielsweise mehrmals zu dem Problem, dass die Tests alle gefailed haben, weil noch der Server aus einer Vorlesung geprüft wurde und nicht mein main.py.


---

#### 3. 💡 How did I overcome them?

Ich habe viel mit den Beispielen aus den Präsentationsfolien gearbeitet und versucht die Beispiele nachzuvollziehen und im Anschluss auf meine Fälle anzuwenden. Dabei hat mir geholfen erstmal mit sehr einfachen Tests zu starten und mich dann graduell zu steigern.
Begriffe wie assert oder requests habe ich separat nachgeschlagen oder mir den Zusammenhang des Testcodes mit meiner main.py von einem LLM erklären lassen.
Besonders geholfen hat mir zudem einfach bewusst falsche Eingaben zu machen, um zu schauen ob die von mir erwarteten Statuscodes und Fehlermeldungen zurückkommen.

---

### Day 5

#### 1. ✅ What did I accomplish?

Heute hab ich gelernt, wie man sicherstellt dass die API nur sinnvolle Daten annimmt und schlechte Eingaben direkt ablehnt, bevor sie überhaupt in die Datenbank kommen.
Konkret hab ich gelernt wie man mit Field() einfache Grenzen setzt wie Mindest- und Maximallängen für Felder wie title, content, category und tags. 
Darüber hinaus hab ich eigene Validierungsregeln mit @field_validator geschrieben – zum Beispiel dass der Titel nach dem Trimmen noch mindestens 3 Zeichen haben muss, dass nur bestimmte Kategorien erlaubt sind, und dass Tags automatisch in Kleinbuchstaben umgewandelt werden usw.
Mit dem model_validator hab ich dann eine Regel eingebaut die zwei Felder gleichzeitig prüft: wenn die Kategorie "work" ist, muss der Tag "work" mit dabei sein. 

Für das Tag Modell hab ich zusätzlich einen @field_validator eingebaut der sicherstellt dass Tag-Namen nur Kleinbuchstaben, Zahlen und Bindestriche enthalten dürfen. Hier hat mir der Codeaufbau aus der Präsentation mit Pattern nicht funktioniert. Das hab ich dann nach etwas Recherche mit re.match() gelöst wobei ich dann mehrere if-Funktionen benutzt habe um die min und max Länge abzufragen und die erlaubten Zeichen die im Pattern waren abzufragen.
Außerdem hab ich gelernt dass man in NoteCreate noch eine Email-Funktion über EmailStr einbauen kann, und mit einem priority Feld vom Typ int die Wichtigkeit einer Notiz angeben kann.

Im Anschluss hab ich dann die test_validation.py Datei aus der Präsentation erstellt die alle Validierungsregeln testet und sie mehrmals durchlaufen lassen, nach kleinen Korrekturen haben dann alle Tests gepassed.




---

#### 2. 🚧 What challenges did I face?

Der schwierigste Teil war der Zusammenhang zwischen NoteCreate, field_validator und model_validator. Ich hab erst nicht verstanden wie der model_validator sich die Daten nimmt die bereits durch den field_validator gelaufen sind. Im Skript fehlte mir eine Erklärung was die importierten Inhalte genau können und wie sie intern funktionieren, was mich etwas verwirrt hat.
Außerdem war mir bei dem Test test_patch_with_empty_body_succeeds nicht klar was genau getestet wird. Der Name sagt "succeeds" aber ich hab zuerst gedacht das Ziel wäre ein 422 zu provozieren, weil es so in der Präsentation steht? dabei soll ja das Gegenteil eintreffen. Ein leerer PATCH Body soll ja gerade erfolgreich sein weil nichts verändert wird, nicht abgelehnt werden, deswegen hab ich den Test jetzt mit einer 200 response geschrieben.
Der pattern Parameter in SQLModel's Field hat beim Start einen TypeError geworfen.
Auch das Löschen der notes.db hat mich Zeit gekostet weil ich nicht sofort verstanden hab warum eine Datenbankstrukturänderung eine frische Datenbank braucht.


---

#### 3. 💡 How did I overcome them?

Den Zusammenhang zwischen field_validator und model_validator hab ich durch Recherche und das konkrete Durcharbeiten eines Beispiels verstanden: field_validator läuft für jedes Feld einzeln, und erst danach bekommt model_validator(mode="after") über self Zugriff auf alle bereits validierten Felder.

Den Testfall test_patch_with_empty_body_succeeds hab ich wie gesagt als 200 response.status_code geschrieben anstatt als 422, ob das richtig ist, weiß ich allerdings nicht. Der Gegensatz dazu, wäre ja eine Rechtmäßige Eingabe eines Titels bzw. eine unrechtmäßige: hier würde dann ein 422 gemeldet, wenn der Titel nach dem trimmen kürzer als 3 Zeichen lang wäre.

Den pattern Bug hab ich gelöst indem ich die Validierung in einen field_validator ausgelagert hab und dort re.match() aus der Python Standardbibliothek verwendet hab. Das hab ich separat nachgeschlagen und dann angewendet.

Generell hat mir wieder geholfen die Fehler im Terminal genau zu lesen und Schritt für Schritt vorzugehen – erst den offensichtlichsten Fehler fixen, Server neu starten, schauen was als nächstes kommt, sowie zwei Terminals nebeneinader zu nutzen beim Testen von test_validation.py


---

### Day 6

#### 1. ✅ What did I accomplish?

Heute hab ich die bestehende API aus den vorherigen Tagen mit dem  Tests aus der Vorlesung von Day 6 laufen lassen und systematisch alle Fehler behoben, bis die Tests durchgelaufen sind.
Dabei hab ich wieder einzelne Fehlermeldungen festigen können, generell läuft die Fehlerbehbeung deutlich schneller als an Tag 1, weil man an Erfahrung hinzugewonnen hat.
Außerdem hab ich verstanden, dass die Reihenfolge der Endpoints für den Durchlauf des Tests wichtig ist. Routen wie /notes/stats müssen immer vor Parametern wie /notes/{note_id} stehen, sonst interpretiert FastAPI den String "stats" als eine ID.
Den Stats-Endpoint hab ich komplett auf die Datenbank umgestellt, weil er vorher noch auf die alte JSON-Datei zugegriffen hat.
Für PUT und PATCH hab ich die fehlende Tag-Logik nachgezogen, sodass Tags beim Update auch wirklich ersetzt werden und nicht einfach ignoriert werden. Zusätzlich hab ich in allen NoteResponse-Rückgaben die fehlenden Felder aus Day 5 priority und author_email ergänzt, die ich beim Erweitern der Endpoints vergessen hatte mitzugeben.


---

#### 2. 🚧 What challenges did I face?


Der größte Fehler war der model_validator aus Tag 5 der verlangte dass jede work-Note den Tag "work" enthält. Das hat fast alle Tests zum Scheitern gebracht weil der Testcode ganz normal work-Notes ohne diesen Tag anlegt.
Danach kamen 500er Fehler – also interne Serverabstürze. Die Fehlermeldung war zwar lang aber eigentlich sehr präzise: AttributeError: 'str' object has no attribute 'name'. Das Problem war dass ich in create_note am Ende note.tags statt db_note.tags verwendet hab.
Außerdem fehlten in ein paar Endpoints priority und author_email im NoteResponse, was ich beim schrittweisen Erweitern des Codes einfach übersehen hatte.


---

#### 3. 💡 How did I overcome them?


Den model_validator hab ich auskommentiert nachdem ich verstanden hab dass er zwar fachlich Sinn ergibt, aber inkompatibel mit dem Test ist.
Den 'str' object has no attribute 'name' Fehler hab ich durch genaues Lesen der Fehlermeldung gefunden – da steht exakt Datei und Zeile drin. Sobald ich verstanden hab was der Unterschied zwischen note und db_note in dem Kontext ist, war der Fix eine einzelne Zeile.
Die fehlenden Felder in NoteResponse hab ich systematisch durch alle Endpoints durchgegangen mit Strg+F nach allen NoteResponse-Stellen geprüft ob priority= und author_email= überall dabei sind.
Nachdem ich diese kleinen Anpassungen gemacht habe lief der Test einwandfrei durch.

---

## Week 3

### Day 7

#### 1. ✅ What did I accomplish?


Heute hab ich zum ersten Mal eine richtige Benutzeroberfläche für meine Notizen API mit Streamlit gebaut.
Für die Hausaufgabe hab ich dann zwei Funktionen in meiner Streamlit App umgesetzt:
Funktion 1 – Alle Notizen anzeigen: Die App holt alle Notizen über einen GET Request von meiner API und zeigt sie als Selectbox an – also als Dropdown mit ID und Titel. Wenn man eine Note auswählt, kann man über einen aufklappbaren Bereich (st.expander) den gesamten Inhalt sehen: Titel, Inhalt, Kategorie, Tags, Priorität und Erstelldatum.
Funktion 2 – Neue Notiz erstellen: Mit st.form hab ich ein Formular gebaut das alle Felder gesammelt abschickt wenn man den Submit-Button drückt. Titel und Inhalt sind Textfelder, die Kategorie eine Selectbox mit den erlaubten Werten, Tags kann man kommagetrennt eingeben und die Priorität lässt sich über einen Slider von 1 bis 5 auswählen. Nach erfolgreichem Erstellen lädt die Seite automatisch neu über st.rerun() damit die neue Notiz direkt in der Liste erscheint.



---

#### 2. 🚧 What challenges did I face?


Schwer gefallen ist mir eigentlich nichts, es hat eigentlich hauptsächlich nur Zeit in Anspruch genommen die einzelnen Streamlit Komponenten zu finden und sich einzulesen. 
Bei den verschiedenen Funktionen wie st.selectbox, st.text_area, st.slider, st.expander musste ich jeweils schauen welche davon für meinen Anwendungsfall passt und wie man sie richtig einsetzt. Ein kleinerer Stolperstein war das Trennen der ausgewählten Note aus der Selectbox – da steht der String "1: Titel" drin und ich musste die ID wieder rausfiltern um damit den richtigen Notizeninhalt zu finden. Das war kein großes Problem, hat aber durchaus etwas Zeit gebraucht in Code umzusetzen.



---

#### 3. 💡 How did I overcome them?

Ich hab parallel mit einem YouTube Video gearbeitet das Streamlit Grundlagen gezeigt hat, das hat mir geholfen die Komponenten schneller zu verstehen als nur durch die Dokumentationen im Internet. Das Aufteilen des ID-Titel-Strings hab ich mit .split(":") gelöst, also indem ich den String am Doppelpunkt trenne und nur den ersten Teil als ID nehmen.
Insgesamt hat mir dieser Tag mit Abstand am meisten Spaß gemacht weil man zum ersten Mal wirklich sieht wie die API die man gebaut hat in einer echten optisch ansprechenden Oberfläche zum Leben erwacht. Der direkte visuelle Feedback macht das ganze viel greifbarer als nur Requests in /docs auszuführen.




---

### Day 8

#### 1. ✅ What did I accomplish?


Heute war ausschließlich die Besprechung zu den hochzuladenden Dateien für die Benotung und den damit zusammenhängenden Formalitäten.



---

#### 2. 🚧 What challenges did I face?



/


---

#### 3. 💡 How did I overcome them?



/


---

### Day 9

#### 1. ✅ What did I accomplish?



/


---

#### 2. 🚧 What challenges did I face?



/


---

#### 3. 💡 How did I overcome them?




/

---


# 🎉 Congratulations! You did it! 🎓✨
#:D












