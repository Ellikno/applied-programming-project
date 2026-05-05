
#Tests für das Main.py mit Vibecoding

import pytest
import requests

BASE_URL = "http://localhost:8000"

# ######################################
# ### Tests für Note API Endpoints
# ######################################

def test_create_note():
    """Testet ob eine neue Note erstellt werden kann"""
    # POST Request mit allen Pflichtfeldern
    response = requests.post(f"{BASE_URL}/notes", json={
        "title": "Test Note",
        "content": "Test Content",
        "category": "work",
        "tags": ["urgent", "meeting"]
    })
    # Prüft ob der Server 201 Created zurückgibt
    assert response.status_code == 201

    data = response.json()


def test_create_note_without_tags():
    """Testet ob eine Note ohne Tags erstellt werden kann"""
    response = requests.post(f"{BASE_URL}/notes", json={
        "title": "Note ohne Tags",
        "content": "Kein Content",
        "category": "personal"
        # tags weggelassen -> sollte trotzdem funktionieren weil  das Tags default [] ist
    })
    assert response.status_code == 201
    data = response.json()


def test_create_note_missing_fields():
    """Testet ob ein Fehler kommt wenn Pflichtfelder fehlen"""
    response = requests.post(f"{BASE_URL}/notes", json={
        "title": "Nur Titel"
        # content und category fehlen -> sollte 422 geben
    })
    assert response.status_code == 422


def test_get_all_notes():
    """Testet ob alle Notes abgerufen werden können"""
    response = requests.get(f"{BASE_URL}/notes")
    # Prüft ob der Server 200 OK zurückgibt
    assert response.status_code == 200
    # Antwort muss eine Liste sein
    assert isinstance(response.json(), list)



def test_get_note_invalid_id():
    """Testet ob ein 404 Fehler kommt wenn die ID nicht existiert"""
    response = requests.get(f"{BASE_URL}/notes/99")
    # 404 = Not Found, also gibts die Note mit dieser ID nicht
    assert response.status_code == 404



def test_patch_note():
    """Testet ob nur einzelne Felder einer Note geändert werden können"""
    # Note erstellen
    create_response = requests.post(f"{BASE_URL}/notes", json={
        "title": "Patch Test",
        "content": "Unveränderter Content",
        "category": "work",
        "tags": []
    })

    #Abfrage der ID der eben erstellten Note, damit man bei dieser Note
    #etwas anpassen kann:
    note_id = create_response.json()["id"]

    # Jetzt ausschließlich den Titel ändern
    response = requests.patch(f"{BASE_URL}/notes/{note_id}", json={
        "title": "Nur Titel geändert"
    })
    assert response.status_code == 200
    data = response.json()
    # Titel wurde geändert
    assert data["title"] == "Nur Titel geändert"


def test_delete_note():
    """Testet ob eine Note gelöscht werden kann"""
    # Note erstellen
    create_response = requests.post(f"{BASE_URL}/notes", json={
        "title": "Löscjen Note",
        "content": "Inhalt",
        "category": "work",
        "tags": []
    })
    note_id = create_response.json()["id"]

    # Note löschen
    response = requests.delete(f"{BASE_URL}/notes/{note_id}")
    # 204 = No Content, erfolgreich gelöscht
    assert response.status_code == 204


def test_delete_note_invalid_id():
    """Testet ob ein 404 Fehler kommt wenn man eine nicht existierende Note löschen will"""
    response = requests.delete(f"{BASE_URL}/notes/87")
    assert response.status_code == 404


def test_get_categories():
    """Testet ob alle Kategorien abgerufen werden können"""
    response = requests.get(f"{BASE_URL}/categories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_notes_by_category():
    """Testet ob Notes nach einer bestimmten Kategorie gefiltert werden können"""
    requests.post(f"{BASE_URL}/notes", json={
        "title": "Kategorie Test",
        "content": "Inhalt",
        "category": "CategoryTests99",
        "tags": []
    })
    response = requests.get(f"{BASE_URL}/categories/CategoryTests99/notes")
    assert response.status_code == 200
    data = response.json()

    for x in data:
        assert x["category"] == "CategoryTests99"


# ######################################
# ### Bonus Challenges: Edge Cases
# ######################################

def test_empty_string_title():
    """Testet ob ein leerer Titel abgelehnt wird"""
    response = requests.post(f"{BASE_URL}/notes", json={
        "title": "",
        "content": "Inhalt",
        "category": "work",
        "tags": []
    })
    # Leerer Titel sollte akzeptiert werden
    assert response.status_code == 201


def test_very_long_content():
    """Testet ob sehr langer Content gespeichert werden kann"""
    long_content = "x" * 1000
    response = requests.post(f"{BASE_URL}/notes", json={
        "title": "Langer Content Test",
        "content": long_content,
        "category": "work",
        "tags": []
    })
    assert response.status_code == 201
    data = response.json()
    # Prüft ob der gesamte Content gespeichert wurde
    assert len(data["content"]) == 1000


def test_special_characters_in_title():
    """Testet ob Sonderzeichen im Titel funktionieren"""
    response = requests.post(f"{BASE_URL}/notes", json={
        "title": "!@#$%^&",
        "content": "Sonderzeichen Test",
        "category": "work",
        "tags": []
    })
    assert response.status_code == 201
    data = response.json()
    # Prüft ob der Titel mit Sonderzeichen korrekt gespeichert wurde
    assert data["title"] == "!@#$%^&"


def test_unicode_in_title():
    """Testet ob Unicode Zeichen wie Emojis oder andere Sprachen funktionieren"""
    response = requests.post(f"{BASE_URL}/notes", json={
        "title": "Unicode Test 🚀 中文 العربية",
        "content": "Inhalt mit Unicode",
        "category": "work",
        "tags": []
    })
    assert response.status_code == 201
    data = response.json()
    # Prüft ob Unicode korrekt gespeichert und zurückgegeben wird
    assert data["title"] == "Unicode Test 🚀 中文 العربية"




# ######################################
# ### Datenbank Tests
# ######################################
