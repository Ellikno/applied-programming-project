from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, Session, create_engine, Relationship, select, or_, col
from typing import Optional, Annotated
from pydantic import BaseModel
from datetime import datetime, timezone
from collections import Counter
import json
from pathlib import Path

app=FastAPI(
    title="Applied Programming Course HS Coburg",
    description="Simple note management API",
    version="1.0.0"
)

#########################################
##### Database Models & Configuration
#########################################
# Definition der Datenbank-Tabellen und Beziehungen
#Anderes Setup als in den Folien zu Präsentation Day 3, da das angegebene nicht funktioniert hat (Hat wohl etwas mit der Version von SQL zu tun.)

class NoteTagLink(SQLModel, table=True):
    note_id: Optional[int] = Field(default=None, foreign_key="notes.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tags.id", primary_key=True)

class Note(SQLModel, table=True):
    __tablename__ = 'notes'
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    category: str
    created_at: datetime = Field(default_factory=datetime.now)
    tags: list["Tag"] = Relationship(back_populates="notes", link_model=NoteTagLink)

class Tag(SQLModel, table=True):
    __tablename__ = 'tags'
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    notes: list[Note] = Relationship(back_populates="tags", link_model=NoteTagLink)

# Create database engine
engine = create_engine("sqlite:///notes.db")

# Create tables (Note, Tag, and link table)
SQLModel.metadata.create_all(engine)

def get_session():
    """Create a new database session for each request"""
    with Session(engine) as session:
        yield session

# Type alias for cleaner code
SessionDep = Annotated[Session, Depends(get_session)]

#########################################
##### API Schemas (Pydantic Models)
#########################################
# Task 6 Step 3 und 4:
# Definition der Datenstrukturen für API-Anfragen und Antworten

# API Input model
class NoteCreate(BaseModel):
    title: str
    content: str
    category: str
    tags: list[str] = []

# Task 4: PATCH Endpoint, Überarbeitung
class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[list[str]] = None
#Optional-> wenn es fehlt, isses automatisch None

# API Output model
class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    category: str
    tags: list[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

#########################################
##### Legacy JSON Storage (Day 2)
#########################################
#Hilfsfunktionen für die ursprüngliche JSON-basierte Speicherung

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

#########################################
##### Note API Endpoints
#########################################

#Task 6 Step 5 Überarbeitung:
@app.post("/notes", status_code=201)
def create_note(note: NoteCreate, session: SessionDep) -> NoteResponse:
    """Create a new note in database"""
    
    # Create note
    db_note = Note(
        title=note.title,
        content=note.content,
        category=note.category
    )
    
    # Get or create tags (case-insensitive, deduplicated)
    tag_objects = []
    seen_tags = set()
    
    for tag_name in note.tags:
        tag_name_lower = tag_name.lower().strip()
        if not tag_name_lower or tag_name_lower in seen_tags:
            continue
        
        seen_tags.add(tag_name_lower)
        
        # Find existing tag or create new one
        statement = select(Tag).where(Tag.name == tag_name_lower)
        existing_tag = session.exec(statement).first()
        
        if existing_tag:
            tag_objects.append(existing_tag)
        else:
            new_tag = Tag(name=tag_name_lower)
            session.add(new_tag)
            tag_objects.append(new_tag)
    
    db_note.tags = tag_objects
    
    session.add(db_note)
    session.commit()
    session.refresh(db_note)  # Get the generated ID and load relationships
    
    # Convert to response model
    return NoteResponse(
        id=db_note.id,
        title=db_note.title,
        content=db_note.content,
        category=db_note.category,
        tags=[tag.name for tag in db_note.tags],
        created_at=db_note.created_at.isoformat()
    )

#app.get überarbeitet/neu eingefügt für Task 6 Step 6: Query Database with Filters
@app.get("/notes")
def list_notes(
    session: SessionDep,
    category: str = None,
    search: str = None,
    tag: str = None
) -> list[NoteResponse]:
    """List notes with filters"""
    
    # Build query
    statement = select(Note)
    
    # Apply filters
    if category:
        statement = statement.where(Note.category == category)
    
    if search:
        search_lower = search.lower()
        statement = statement.where(
            or_(
                col(Note.title).ilike(f"%{search_lower}%"),
                col(Note.content).ilike(f"%{search_lower}%")
            )
        )
    
    if tag:
        tag_lower = tag.lower()
        statement = statement.join(Note.tags).where(Tag.name == tag_lower)
    
    # Execute query
    notes = session.exec(statement).all()
    
    # Convert to response models
    return [
        NoteResponse(
            id=n.id,
            title=n.title,
            content=n.content,
            category=n.category,
            tags=[tag.name for tag in n.tags],
            created_at=n.created_at.isoformat()
        )
        for n in notes
    ]

#Task 6 Step 7: Überarbeitung der Endpoints
@app.get("/notes/{note_id}")
def get_note(note_id: int, session: SessionDep) -> NoteResponse:
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteResponse(
        id=note.id,
        title=note.title,
        content=note.content,
        category=note.category,
        tags=[tag.name for tag in note.tags],
        created_at=note.created_at
    )

@app.put("/notes/{note_id}")
def update_note(note_id: int, note_update: NoteCreate, session: SessionDep) -> NoteResponse:
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note.title = note_update.title
    note.content = note_update.content
    note.category = note_update.category
    session.add(note)
    session.commit()
    session.refresh(note)
    return NoteResponse(
        id=note.id,
        title=note.title,
        content=note.content,
        category=note.category,
        tags=[tag.name for tag in note.tags],
        created_at=note.created_at
    )

@app.patch("/notes/{note_id}")
def partial_update_note(note_id: int, note_update: NoteUpdate, session: SessionDep) -> NoteResponse:
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note_update.title is not None:
        note.title = note_update.title
    if note_update.content is not None:
        note.content = note_update.content
    if note_update.category is not None:
        note.category = note_update.category
    session.add(note)
    session.commit()
    session.refresh(note)
    return NoteResponse(
        id=note.id,
        title=note.title,
        content=note.content,
        category=note.category,
        tags=[tag.name for tag in note.tags],
        created_at=note.created_at
    )
#nur die Überarbeiteten werden mitgeschickt,also für den Fall,
#dass es nicht None ist, wird es überschrieben

@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, session: SessionDep):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    session.delete(note)
    session.commit()
    return

    #ID 6 wurde angelegt mit: {"title": "New", "content": "New", "category": "work", "tags": []}
    #in Patch wurde dann ausschließlich der Titel mit: {"title": "Just change title"} überschrieben

#########################################
##### Tag & Category Endpoints
#########################################
#Endpunkte zur Verwaltung von Tags und Kategorien

#Task 6 Step 8: Tag Endpoints hinzufügen
@app.get("/tags")
def list_tags(session: SessionDep) -> list[str]:
    """Get all unique tags from the Tag table"""
    statement = select(Tag)
    tags = session.exec(statement).all()
    
    return sorted([tag.name for tag in tags])

@app.get("/tags/{tag_name}/notes")
def get_notes_by_tag(tag_name: str, session: SessionDep) -> list[NoteResponse]:
    """Get all notes with specific tag"""
    
    # Find the tag (case-insensitive)
    tag_lower = tag_name.lower()
    statement = select(Tag).where(Tag.name == tag_lower)
    tag = session.exec(statement).first()
    
    if not tag:
        return []  # No notes if tag doesn't exist
    
    # Return all notes associated with this tag
    return [
        NoteResponse(
            id=note.id,
            title=note.title,
            content=note.content,
            category=note.category,
            tags=[t.name for t in note.tags],
            created_at=note.created_at
        )
        for note in tag.notes
    ]

# Task 3: Categories Resource
@app.get("/categories")
def list_categories(session: SessionDep) -> list[str]:
    notes = session.exec(select(Note)).all()
    
    categories = set()
    for note in notes:
        categories.add(note.category)
    
    return sorted(list(categories))
#Gibt eine Liste aus, in der jede Kategorie unabhänig davon wie oft sie existiert
#nur einmal ausgegeben wird -> ich sehe welche Kategorien es gibt!

@app.get("/categories/{category_name}/notes")
def get_notes_by_category_resource(category_name: str, session: SessionDep) -> list[NoteResponse]:
    statement = select(Note).where(Note.category == category_name)
    notes = session.exec(statement).all()
    
    return [
        NoteResponse(
            id=note.id,
            title=note.title,
            content=note.content,
            category=note.category,
            tags=[tag.name for tag in note.tags],
            created_at=note.created_at
        )
        for note in notes
    ]
#Gibt mir wenn ich nach dem category_name suche alle Notizen aus, die 
#den gesuchten category_name/die Kategorie x haben. Bei "work" sind das
#id1,2 und 4

#########################################
##### Statistics
#########################################

#Task 2: Statistic Endpoints
@app.get("/notes/stats")
def get_notes_stats():
    notes_db, _ = load_notes()

    category_counts = Counter(note.category for note in notes_db)

    all_tags = []
    for note in notes_db:
        for tag in note.tags:
            all_tags.append(tag)

    tag_counts = Counter(all_tags)

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

#Homework Day 3 Implication (Task 1-tags + Datumabfrage(Task5)):
#Endpoints für Notizen-Suche in der JSON-Datei
@app.get("/notes/legacy")
def list_notes_legacy(
    category: str = None,
    search: str = None,
    tag: str = None,
    created_after: str = None,
    created_before: str = None
) -> list[Note]:
    """
    List notes with optional filters (JSON Version)
    
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

#########################################
##### Vorlesung Tag 3
#########################################

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