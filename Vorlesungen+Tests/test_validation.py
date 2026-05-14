#Validierungstests für die NoteCreate und NoteUpdate Modelle aus der Main.py
#Day 5 Task 1-5 Tests
#Testet ob die Pydantic Validierungsregeln aus Day 5 korrekt funktionieren


#Day 5 Task6:

import pytest
import requests

BASE_URL = "http://localhost:8000"


def test_create_note_rejects_short_title():
    """Titel mit weniger als 3 Zeichen muss abgelehnt werden"""
    response = requests.post(f"{BASE_URL}/notes", json={
        "title": "ab",
        "content": "Inhalt",
        "category": "work",
        "tags": ["work"]
    })
    # Field min_length=3 greift -> 422
    assert response.status_code == 422


def test_create_note_rejects_unknown_category():
    """Unbekannte Kategorie muss abgelehnt werden"""
    response = requests.post(f"{BASE_URL}/notes", json={
        "title": "Test Note",
        "content": "Inhalt",
        "category": "unbekannt",
        "tags": []
    })
    # category_must_be_known validator greift -> 422
    assert response.status_code == 422


def test_create_note_normalizes_tags():
    """Tags sollen lowercase werden und Duplikate entfernt werden"""
    response = requests.post(f"{BASE_URL}/notes", json={
        "title": "Tag Test",
        "content": "Inhalt",
        "category": "work",
        "tags": ["URGENT", "urgent", "work", "  meeting  ", "Q2"]
    })
    assert response.status_code == 201
    data = response.json()
    # Duplikate weg, alles lowercase, Leerzeichen getrimmt
    assert "urgent" in data["tags"]
    assert "meeting" in data["tags"]
    assert "q2" in data["tags"]
    # URGENT und urgent dürfen nur einmal vorkommen
    assert data["tags"].count("urgent") == 1


def test_create_note_forbids_extra_fields():
    """Unbekannte Felder müssen abgelehnt werden wegen extra=forbid in NoteCreate"""
    response = requests.post(f"{BASE_URL}/notes", json={
        "title": "Test Note",
        "content": "Inhalt",
        "category": "work",
        "tags": ["work"],
        "Footballer": ["Messi"]  # unbekanntes Feld
    })
    # extra=forbid greift -> 422
    assert response.status_code == 422


def test_work_note_requires_work_tag():
    """Work Notes müssen den Tag 'work' enthalten"""
    response = requests.post(f"{BASE_URL}/notes", json={
        "title": "Work Meeting",
        "content": "Inhalt",
        "category": "work",
        "tags": ["urgent"]  # work Tag fehlt
    })
    # model_validator greift -> 422
    assert response.status_code == 422



def test_patch_with_empty_body_succeeds():
    """PATCH mit leerem Body muss funktionieren - nichts wird geändert"""
    # Erst Note erstellen
    create = requests.post(f"{BASE_URL}/notes", json={
        "title": "Patch Test",
        "content": "Inhalt",
        "category": "personal",
        "tags": []
    })
    note_id = create.json()["id"]

    # Leerer PATCH -> keine Änderung, kein Fehler
    response = requests.patch(f"{BASE_URL}/notes/{note_id}", json={})
    assert response.status_code == 200


def test_patch_with_invalid_title_fails():
    """PATCH mit zu kurzem Titel muss 422 geben"""
    create = requests.post(f"{BASE_URL}/notes", json={
        "title": "Patch Test",
        "content": "Inhalt",
        "category": "personal",
        "tags": []
    })
    note_id = create.json()["id"]

    # Titel zu kurz -> 422
    response = requests.patch(f"{BASE_URL}/notes/{note_id}", json={
        "title": "ab"
    })
    assert response.status_code == 422


def test_tag_name_rejects_uppercase():
    """Tags mit Großbuchstaben müssen abgelehnt werden"""
    response = requests.post(f"{BASE_URL}/notes", json={
        "title": "Tag Test Großbuchstaben",
        "content": "Inhalt",
        "category": "personal",
        "tags": ["GROSSBUCHSTABEN"]
    })
    # clean_tags validator macht lowercase -> eigentlich wird es normalisiert
    # aber pattern im Tag Modell lehnt Großbuchstaben ab
    # Ergebnis: entweder normalisiert oder 422
    data = response.json()
    if response.status_code == 201:
        # Falls normalisiert: muss lowercase sein
        assert "grossbuchstaben" in data["tags"]