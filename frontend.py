#- Streamlit Installieren
#- Streamlit App "Hello, World!" erstellen und testen
#- "Say no" - App als ersten Test erstellen
 # - API Documentation: https://github.com/hotheadhacker/no-as-a-service
 # - API Endpoint: https://naas.isalman.dev/no
 # - Button in Streamlit, der bei Klick eine Anfrage an den API Endpoint sendet und die Antwort anzeigt

#- Todos für Nachmittag:
#  - Streamlit App mit 2 Funktionen von Notizen API
#  - Funktion 1: Alle Notizen anzeigen
#    - Liste von Titeln von Notizen anzeigen
#    - Möglichkeit zu einem Titel den Inhalt, Tags, Category, etc. anzuzeigen
#  - Funktion 2: Neue Notiz erstellen (Formular mit Titel und Inhalt, Button)
#    - Erstellen einer neuen Notiz (Titel, Inhalt, Tags, Category)
#    - Neu erstellte Notiz soll in Liste auftauchen


import streamlit as st
import requests
 
#########################
 #Aus der Vorlesung:
#########################
#URL = "https://naas.isalman.dev/no"
 
#def request_no():
#    response = requests.get(URL)
#    response_json = response.json()
#    return response_json["reason"]
 
# Initialization
#if 'text1' not in st.session_state:
#    st.session_state['text1'] = request_no()
#    print("init Text1")
 
#if 'text' not in st.session_state:
#    st.session_state['text'] = request_no()
#    print("init Text")
 
#name = st.text_input("Name", placeholder="Hier Name eingeben...")
#st.write(name)
 
#if st.button("Neuer Text1"):
#    st.session_state['text1'] = request_no()
 
#st.write(st.session_state["text1"])
 
 
#if st.button("Neuer Text"):
#    st.session_state['text'] = request_no()
 
#st.write(st.session_state["text"])
 
 
#with st.expander('session state'):
#    st.write(st.session_state)
 

#################################################
#Hausaufgabe: Notizen anzeigen und neue erstellen
#################################################

###################################
#Funktion 1: Alle Notizen anzeigen
###################################

API_URL = "http://localhost:8000"

#Überschrift:
st.title("Notizen App")


#Unterüberschrift:
st.header("Alle Notizen")

#Alle Notizen holen:
response = requests.get(f"{API_URL}/notes")
if response.status_code == 200:
    notes = response.json()
else:
    notes = []
    st.error("Fehler beim Laden der Notizen")

#Alle Notizen auf der Website anzeigen lassen mit ID und Titel
if notes:
    titles = []
    for n in notes:
        #ID und Titel als zusammenhängenden String appenden
        titles.append(f"{n['id']}: {n['title']}")

#Hier sind jetzt alle Notizen aufgelistet mit ID und Titel
    selected = st.selectbox("Notiz auswählen", titles)

#Notiz am ":" trennen um ID und Titel wieder einzeln zu haben:
    selected_id = int(selected.split(":")[0])

#Jetzt wieder den gesamten Notizeninhalt der Note finden
#durch Vergleichen der IDs
    note = None
    for n in notes:
        if n["id"] == selected_id:
            note = n
            break


#Erstellen einer "Box-Funktion" auf der Website mit den darin
#notwendigen Notizinhalten (Bei laden der Website ist sie geschlossen bzw. aufklappbar)
    with st.expander("Notizeninhalt anzeigen", expanded=False):
        #Schreibt mir den gesamten Inhalt der Note dessen ID ich ausgewählt habe:
         st.write(f"Titel: {note['title']}")
         st.write(f"Inhalt: {note['content']}")
         st.write(f"Kategorie: {note['category']}")
         st.write(f"Tags: {', '.join(note['tags']) if note['tags'] else '–'}")
         st.write(f"Priorität: {note['priority']}")
         st.write(f"Erstellt: {note['created_at']}")
else:
    st.info("Noch keine Notizen vorhanden.")




#################################
#Funktion 2: Neue Notiz erstellen
#################################


#2te Unterüberschrift auf der Website:
st.header("Neue Notiz erstellen")

#St.form sammelt die Eingabefelder values und schickt sie gebündelt
#nach der Notizeingabe durch betätigen des Submit-Buttons ab:
with st.form("create_note_form"):

    title = st.text_input("Titel") #Ein Textfeld
    content = st.text_area("Inhalt") #Großes Textfeld
    category = st.selectbox(  #Selectbox der angegebenen Kategorienn
        "Kategorie",
        ["work", "personal", "school", "study", "ideas", "general"]
    )
    tags_input = st.text_input("Tags (kommagetrennt, z.B. python, api)")
    priority = st.slider("Priorität", 1, 5, 3) #Priorität mit Slider Funktion auswählbar
    submitted = st.form_submit_button("Notiz erstellen") #Button auf dem 'Notiz erstellen' steht


#Submit Button wurde geklickt, dann gehts hier weiter:
if submitted:
    #Tags werden getrennt und als Liste gespeichert
    tags = [t.strip() for t in tags_input.split(",") if t.strip()]

#Datenpaket das dann letztendlich an meine API geschickt wird
#Hier werden die Eingaben aus st.form gesammelt
    payload = {
        "title": title,
        "content": content,
        "category": category,
        "tags": tags,
        "priority": priority
    }
    #Post Request an die API
    result = requests.post(f"{API_URL}/notes", json=payload)

    #Abfrage ob das erstellen der Notiz erfolgreich war
    #Wenn erfolglos dann wird die Fehlermeldung ausgegeben
    if result.status_code == 201:
        st.write("Notiz wurde erfolgreich erstellt")
        st.rerun() #Lädt die Streamlit Seite neu bei erfolgreicher Note Erstellung
    else:
        st.write(f"Fehler: {result.json()}") 



