
from fastapi import FastAPI, HTTPException



from pydantic import BaseModel
from datetime import datetime, timezone
from typing import Optional
from collections import Counter
import json
from pathlib import Path

app=FastAPI(
    title="Applied Programming Course HS Coburg",
    description="Simple note management API",
    version="1.0.0"
)


#########################################
##### Note API Endpoints (Day 2)
#########################################

class NoteCreate(BaseModel):
    title:str
    content:str
    category: str 
    tags: list[str] = []

class Note(BaseModel):
    id: int
    title: str
    content: str
    category: str
    tags: list[str] = []
    created_at: str

NOTES_FILE = Path("data/notes.json")

def load_notes():
    """Load notes from JSON file and return notes list and next ID counter"""
    notes_db = []
    note_id_counter = 1

    if NOTES_FILE.exists():
        with open(NOTES_FILE, 'r') as f:
            data = json.load(f)
            notes_db = [Note(**note) for note in data]

            # Set counter to max ID + 1
            if notes_db:
                note_id_counter = max(note.id for note in notes_db) + 1

    return notes_db, note_id_counter


def save_notes(notes_db):
    """Save notes to JSON file after each change"""
    # Ensure data directory exists
    NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)
    print("Saving to:", NOTES_FILE.resolve())

    with open(NOTES_FILE, 'w') as f:
        # Convert Note objects to dicts
        notes_data = [note.dict() for note in notes_db]
        json.dump(notes_data, f, indent=2)


@app.post("/notes" , status_code=201)
def create_note(note: NoteCreate) -> Note:

    """Create a new note"""

    notes_db, note_id_counter = load_notes()

    new_note = Note(
        id=note_id_counter,
        title=note.title,
        content=note.content,
        category=note.category,
        tags=note.tags,
        created_at=datetime.now(timezone.utc).isoformat()

    )
    notes_db.append(new_note)
    note_id_counter += 1
    save_notes(notes_db)
    return new_note


############################################
######  Homework Day 2
############################################

#Categorys eingefügt in class Note(BaseModel)

@app.get("/notes/category/{category}")
def get_notes_by_category(category: str):
    """Get all notes in a specific category"""
    notes_db, _ = load_notes()
    filtered_notes = []
    
    for note in notes_db:
        if note.category == category:
            filtered_notes.append(note)
    
    return filtered_notes


################################
## Crud Points
################################
#Lesson Day 3:
@app.get("/queryparameters")
def queryparameters(param1: str=None, param2: int=None) -> dict:

    """Example endpoint to demonstrate query parameters

    -**param**: A string parameter (optional)
    -**param2**: An integer parameter (optional)

    Returns a JSON object with the provided parameters
    """
    namen= ["Martin" ,"Sophie" ,"Michael","Elias"]

    if not param1:
        return{"namen": namen}
    
    namen_gefiltert= []
    for name in namen:
        print(name)
        if param1 and param1 in name:
            namen_gefiltert.append(name)


    return {
        "param1":param1,
        "param2":param2,
        "namen":namen_gefiltert
    }

######################################
### Homework Day 3
######################################


#Homework Day 3 Implication (Task 1-tags + Datumabfrage(Task5)):
@app.get("/notes")
def list_notes(
    category: str = None,
    search: str = None,
    tag: str = None,
    created_after: str = None,
    created_before: str = None
) -> list[Note]:
    """
    List notes with optional filters
    
    - category: Filter by category
    - search: Search in title and content
    - tag: Filter by tag
    - created_after: Only notes created after this date (ISO format: 2026-04-01)
    - created_before: Only notes created before this date (ISO format: 2026-04-30)
    """
    notes_db, _ = load_notes()
    
    # Apply filters
    filtered = []
    for note in notes_db:
        # Filter by category
        if category and note.category != category:
            continue
        
        # Filter by search term
        if search:
            search_lower = search.lower()
            title_match = search_lower in note.title.lower()
            content_match = search_lower in note.content.lower()
            if not (title_match or content_match):
                continue
        
        # Filter by tag
        if tag and tag not in note.tags:
            continue
        
        #ganz normal die bisherigen Filterungs Paramater


        # Filter by date range
        if created_after and note.created_at < created_after:
            continue
        
        if created_before and note.created_at > created_before:
            continue
        
        filtered.append(note)

        #Datumsabfrage- welche Notizen wurden vor bzw. nach Datum xy erstellt
        #Jetzt sind auch Datumsabfragen in Kombi mit den anderen Parametern möglich
        #zB welche Notizen der Kategorie work wurden nach Datum xy erstellt?

    print(NOTES_FILE.resolve())
    return filtered

#Task 2: Statistic Endpoints

@app.get("/notes/stats")
def get_notes_stats():
    """Get statistics about notes"""
    notes_db, _ = load_notes()

    # Count by category
    #From collections import counter noch oben in die Imports aufgenommen
    category_counts = Counter(note.category for note in notes_db)

    # Collect all tags from all notes
    all_tags = []
    for note in notes_db:
        for tag in note.tags:
            all_tags.append(tag)

    # Count tags
    tag_counts = Counter(all_tags)

    # Top 5 tags formatted
    top_tags = [
        {"tag": tag, "count": count}
        for tag, count in tag_counts.most_common(5)
    ]

    return {
        "total_notes": len(notes_db),
        "by_category": dict(category_counts),
        "top_tags": top_tags,
        "unique_tags_count": len(tag_counts)

    #zählt alle Notizen, Notizen pro Kategorie, Welche tags am häufigsten vorkommen
    # wie viele verschiedene tags es überhaupt gibt
    }


# Task 3: Categories Resource
@app.get("/categories")
def list_categories() -> list[str]:
    """Get all unique categories from all notes"""
    notes_db, _ = load_notes()
    
    # Collect unique categories
    categories = set()
    for note in notes_db:
        categories.add(note.category)
    
    # Return sorted list
    return sorted(list(categories))

#Gibt eine Liste aus, in der jede Kategorie unabhänig davon wie oft sie existiert
#nur einmal ausgegeben wird -> ich sehe welche Kategorien es gibt!

@app.get("/categories/{category_name}/notes")
def get_notes_by_category_resource(category_name: str) -> list[Note]:
    """Get all notes in a specific category"""
    notes_db, _ = load_notes()
    
    # Filter notes by category
    filtered = []
    for note in notes_db:
        if note.category == category_name:
            filtered.append(note)
    
    return filtered

#Gibt mir wenn ich nach dem category_name suche alle Notizen aus, die 
#den gesuchten category_name/die Kategorie x haben. Bei "work" sind das
#id1,2 und 4


# Task 4: PUT Endpoint (komplettes Update)
@app.put("/notes/{note_id}")
def update_note(note_id: int, note_update: NoteCreate) -> Note:
    """Update an existing note completely"""
    notes_db, _ = load_notes()
    
    for i, note in enumerate(notes_db):
        if note.id == note_id:
            updated_note = Note(
                id=note.id,
                title=note_update.title,
                content=note_update.content,
                category=note_update.category,
                tags=note_update.tags,
                created_at=note.created_at
            )
            notes_db[i] = updated_note
            save_notes(notes_db)
            return updated_note
    
    raise HTTPException(
        status_code=404,
        detail=f"Note with ID {note_id} not found"
    )


# Task 4: PATCH Endpoint, Überarbeitung
class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[list[str]] = None
#Optional-> wenn es fehlt, isses automatisch None

@app.patch("/notes/{note_id}")
def partial_update_note(note_id: int, note_update: NoteUpdate) -> Note:
    """
    Partially update a note (only provided fields)
    
    Unlike PUT, PATCH only updates fields you provide
    """
    notes_db, _ = load_notes()
    
    for i, note in enumerate(notes_db):
        if note.id == note_id:
            if note_update.title is not None:
                note.title = note_update.title
            if note_update.content is not None:
                note.content = note_update.content
            if note_update.category is not None:
                note.category = note_update.category
            if note_update.tags is not None:
                note.tags = note_update.tags
            #nur die Überarbeiteten werden mitgeschickt,also für den Fall,
            #dass es nicht None ist, wird es überschrieben
            notes_db[i] = note
            save_notes(notes_db)
            return note
    
    raise HTTPException(
        status_code=404,
        detail=f"Note with ID {note_id} not found"
    #ID 6 wurde angelegt mit: {"title": "New", "content": "New", "category": "work", "tags": []}
    #in Patch wurde dann ausschließlich der Titel mit: {"title": "Just change title"} überschrieben
    )

#Task 5 Erweiterung des bestehenden GET/notes Endpoint um Erstelldatumsabfrage
#-> Code unter Task 1 eingefügt


#Task6 Database Migration





