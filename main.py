from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, Session, create_engine, Relationship, select, or_, col
from typing import Optional, Annotated
from pydantic import BaseModel
from datetime import datetime, timezone
from collections import Counter
import json
from pathlib import Path
from pydantic import BaseModel, ConfigDict, field_validator, model_validator, EmailStr
from typing_extensions import Self

app=FastAPI(
    title="Applied Programming Course HS Coburg",
    description="Simple note management API",
    version="1.0.0"
)

#########################################
##### Database Models and Configuration
#########################################
# Definition der Datenbank-Tabellen und Beziehungen


#Anpassung Day 6 Test
@app.get("/")
def root():
    return {"title": app.title, "version": app.version}

###########################

# NoteTagLink ist eine Verbindungstabelle zwischen Notes und Tags (Many-to-Many)
# Eine Note kann mehrere Tags haben, ein Tag kann aber auf mehreren Notes sein
# SQLModel erstellt diese Tabelle nicht automatisch (Versions-Problem), deswegen
# wird sie hier explizit definiert.

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
#Zusatzaufgabe Email Day 5 Task "7":
    author_email: Optional[str] = None
    priority: int = Field(default=3, ge=1, le=5)


#Day 5 Task 5 Validation hinzugefügt für die Tags
class Tag(SQLModel, table=True):
    __tablename__ = 'tags'
    id: Optional[int] = Field(default=None, primary_key=True)
    #name muss 2-30 Zeichen haben, Kleinbuchstaben(a-z), Zahlen(0-9) und Bindestriche sind erlaubt
    name: str = Field(unique=True, index=True)
    notes: list[Note] = Relationship(back_populates="tags", link_model=NoteTagLink)

    @field_validator("name")
    @classmethod
    def allowed_name(cls, value: str) -> str:
        #Erst trimmen und lowercase machen
        normalized = value.strip().lower()
        #Dann prüfen ob das Pattern passt - nur a-z, 0-9 und Bindestriche erlaubt
        import re
        if not re.match(r"^[a-z0-9-]+$", normalized):
            raise ValueError("Tag name darf nur Kleinbuchstaben, Zahlen und Bindestriche enthalten")
        #Mindest- und Maximallänge prüfen
        if len(normalized) < 2:
            raise ValueError("Tag name muss mindestens 2 Zeichen haben")
        if len(normalized) > 30:
            raise ValueError("Tag name darf maximal 30 Zeichen haben")
        return normalized


# Create database engine
engine = create_engine("sqlite:///notes.db")

# Create tables (Note, Tag, and link table)
SQLModel.metadata.create_all(engine)

def get_session():
    """Create a new database session for each request"""
    with Session(engine) as session:
        yield session

# Type alias for cleaner code
#SessionDep ist eine Abkürzung damit man nicht jedes Mal den vollen Typ ausschreiben muss
# Depends(get_session) sagt FastAPI: erstelle für jeden Request eine neue Session
# und schließe sie danach automatisch wieder
# Annotated verknüpft den Typ Session mit der Depends-Anweisung zu einem einzigen Parameter
SessionDep = Annotated[Session, Depends(get_session)]
#Aus Vorlesungsfolie Day 3:
#FastAPI will automatically:
    #Create a new session for each request
    #Close the session when done
    #Handle database transactions



#########################################
##### API Schemas (Pydantic Models)
#########################################
# Day 3 Task 6 Step 3 und 4:
# Definition der Datenstrukturen für API-Anfragen und Antworten
# API Input model
# Day 5 Task 1-2: Validation Grenzen bzw. Regeln für die Eingaben in
#Title, Categories und Tags festgelegt

ALLOWED_CATEGORIES = {"work", "personal", "school", "study", "ideas", "general"}
class NoteCreate(BaseModel):
    model_config= ConfigDict(
        str_strip_whitespace=True, #Strings werden automatisch getrimmt zB. "  Brot  " -> "Brot"
        extra="forbid" #unbekannte Angaben werden abgelehnt
    )
    title: str = Field(min_length=3, max_length=100)
    content: str = Field(min_length=1, max_length=10_000)
    category: str = Field(min_length=2, max_length=30)
    tags: list[str] = Field(default_factory=list, max_length=10)
#Zusatzaufgabe Email Day 5 Task "7":
    author_email: EmailStr | None=None
    priority: int = Field(default=3, ge=1, le=5)

# Lehnt Titel ab, die nur aus Leerzeichen bestehen und Titel muss >3 sein nach dem Trimmen
    @field_validator("title")
    @classmethod
    def title_not_only_whitespace(cls, value: str) -> str:
        # Nach dem Trimmen muss noch mindestens 3 Zeichen übrig sein
        if len(value.strip()) < 3:
            raise ValueError("Titel darf nicht nur aus Leerzeichen bestehen")
        return value

#Beschränkt die erlaubten Kategorien auf die Angaben innerhalb von "ALLOWED_CATEGORIES"
    @field_validator("category")
    @classmethod
    def category_must_be_known(cls, value: str) -> str:
        # Erst lowercase machen, dann prüfen
        normalized = value.strip().lower()
        if normalized not in ALLOWED_CATEGORIES:
            raise ValueError(
                f"category muss eine der folgenden sein: {sorted(ALLOWED_CATEGORIES)}"
            )
        return normalized


    @field_validator("tags")
    @classmethod
    def clean_tags(cls, raw: list[str]) -> list[str]:
        cleaned = []
        seen = set()
        for tag in raw:
            t = tag.strip().lower()
            # Leere Tags werden abgelehnt
            if not t:
                raise ValueError("Tags dürfen keine leeren Strings sein")
            # Tags kürzer als 2 Zeichen ablehnen
            if len(t) < 2:
                raise ValueError("Tags müssen mindestens 2 Zeichen haben")
            # Duplikate überspringen/nicht mit aufnehmen in tags
            if t in seen:
                continue
            seen.add(t)
            cleaned.append(t)
        return cleaned

#Day 5 Task 3: Model Validator hinzufügen und erklären

    #@model_validator(mode="after")
    #def work_notes_need_work_tag(self) -> Self:
        #if self.category == "work" and "work" not in self.tags:
            #raise ValueError("work notes must include the 'work' tag")
        #return self 
#(Im Nachhinein auskommentiert da es für Day 6 Test irrelevant ist und viele Tests failen lässt)

#Erklärung:
# Da eine Abhängigkeit zwischen zwei Feldern geprüft werden soll (category und tags), wird
#model_validator benötigt (field prüft immer nur einzelne Felder)
# Der Model_validator wird erst aufgerufen nachdem alle field Funktionen durch sind (mode="after")
# Das self erhebt dann die Daten und prüft ob der Zusammenhang zwischen category und tag passt


# Day 3 Task 4: PATCH Endpoint, Überarbeitung
##Update Day5 Task 4: Fields hinzugefügt von Pydantic für Validation /Begrenzung der Eingabedaten
#(NoteCreate (input) and NoteUpdate (partial input) should share validation.)

class NoteUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=100)
    content: str | None = Field(default=None, min_length=1)
    category: str | None = None
    tags: list[str] | None = Field(default=None, max_length=10)
    priority: int | None = Field(default=None, ge=1, le=5)
# Datentyp | None bedeutet: Entweder Datentyp x wie zB. string oder None. 
#Wenn ein str mitgeschickt wird, greift die Field Regel für zB. den Titel nach dem in der Präsentation
#erklärten Prinzip: PATCH with {} must succeed (no changes). PATCH with {"title": ""} must return 422 (Field check passt).



# API Output model
class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    category: str
    tags: list[str]
    created_at: datetime
#Zusatzaufgabe Email Day 5 Task "7":
    priority: int
    author_email: str | None
    
    class Config:
        from_attributes = True

#########################################
##### JSON Storage (Day 2)
#########################################
#Hilfsfunktionen für die ursprüngliche JSON-basierte Speicherung

# load_notes() und save_notes() sind die ursprünglichen Hilfsfunktionen aus Day 2 Step 12+13
# seit Day 3 Task 6 (Datenbank Einführung) werden sie nicht mehr für die Haupt-Endpoints verwendet
# Sie sind noch drin weil /notes/legacy und /notes/stats sie noch nutzen
# und um den Entwicklungsfortschritt von JSON-Datei zu Datenbank nachvollziehbar für mich
# zu machen

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

#Day 3 Task 6 Step 5 Überarbeitung:
@app.post("/notes", status_code=201)
def create_note(note: NoteCreate, session: SessionDep) -> NoteResponse:
    """Create a new note in database"""
    
    # Create note
    db_note = Note(
        title=note.title,
        content=note.content,
        category=note.category,
        priority=note.priority,  #Zusatzaufgabe Email Day 5 Task "7",
        #Beim erstellen der Note kann der Autor angeben wie wichtig(Weltuntergang) oder unwichtig(Kaffeebohnen leer) die Notiz ist
        author_email=note.author_email #Zusatzaufgabe Email Day 5 Task "7"
    )
    
    # Get or create tags (case-insensitive, deduplicated)
    tag_objects = []
    seen_tags = set()
    
    for tag_name in note.tags:
        tag_name_lower = tag_name.lower().strip()
        if not tag_name_lower or tag_name_lower in seen_tags:
            continue
        
        seen_tags.add(tag_name_lower)

        # Erst prüfen ob der Tag bereits in der Datenbank existiert
        # Wenn ja: bestehenden Tag nehmen statt einen neuen anzulegen
        # Wenn nein: neuen Tag erstellen
        # Das verhindert Duplikate in der Tags-Tabelle – "urgent" soll
        # nur einmal existieren egal wie viele Notes diesen Tag haben
        
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
    # Nach dem commit kennt die Datenbank die generierte ID und alle verknüpften Tags
    # session.refresh() holt diese aktualisierten Daten zurück ins Python-Objekt
    # Ohne refresh() hätte db_note noch keine ID und note.tags wäre leer
    session.refresh(db_note) 
    
    # Convert to response model
    return NoteResponse(
        id=db_note.id,
        title=db_note.title,
        content=db_note.content,
        category=db_note.category,
        tags=[tag.name for tag in db_note.tags],
        created_at=db_note.created_at.isoformat(),
        priority=db_note.priority,
        author_email=db_note.author_email
    )

#app.get überarbeitet/neu eingefügt für Task 6 Step 6: Query Database with Filters
@app.get("/notes")
def list_notes(
    session: SessionDep,
    category: str = None,
    search: str = None,
    tag: str = None,
    created_after: datetime = None,   #Implementierung Day 6 Test
    created_before: datetime = None   #Implementierung Day 6 Test
) -> list[NoteResponse]:

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

    if created_after:
        notes = [n for n in notes if n.created_at >= created_after]
    if created_before:
        notes = [n for n in notes if n.created_at <= created_before]
    
    # Convert to response models
    return [
        NoteResponse(
            id=n.id,
            title=n.title,
            content=n.content,
            category=n.category,
            tags=[tag.name for tag in n.tags],
            created_at=n.created_at, priority=n.priority, 
            author_email=n.author_email
        )
        for n in notes
    ]



#Day 3 Task 2: Statistic Endpoints angelegt
# und auf Datenbank umgestellt
@app.get("/notes/stats")
def get_notes_stats(session: SessionDep):
    notes = session.exec(select(Note)).all()

    category_counts = Counter(note.category for note in notes)

    all_tags = []
    for note in notes:
        for tag in note.tags:
            all_tags.append(tag.name)

    tag_counts = Counter(all_tags)

    #Alle Tags direkt holen:
    all_unique_tags = session.exec(select(Tag)).all()

    top_tags = [
        {"tag": tag, "count": count}
        for tag, count in tag_counts.most_common(5)
    ]

    return {
        "total_notes": len(notes),
        "by_category": dict(category_counts),
        "top_tags": top_tags,
        "unique_tags_count": len(all_unique_tags)

    #zählt alle Notizen, Notizen pro Kategorie, Welche tags am häufigsten vorkommen
    # und wie viele verschiedene tags es überhaupt in der DB gibt
    }


#Day 3 Task 6 Step 7: Überarbeitung der Endpoints
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
        created_at=note.created_at,
        priority=note.priority,        
        author_email=note.author_email
    )

@app.put("/notes/{note_id}")
def update_note(note_id: int, note_update: NoteCreate, session: SessionDep) -> NoteResponse:
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note.title = note_update.title
    note.content = note_update.content
    note.category = note_update.category
    note.priority = note_update.priority
    note.author_email = note_update.author_email

#Implementierung Day 6 Test: Tags ergänzen
    tag_objects = []
    seen_tags = set()
    for tag_name in note_update.tags:
        tag_name_lower = tag_name.lower().strip()
        if not tag_name_lower or tag_name_lower in seen_tags:
            continue
        seen_tags.add(tag_name_lower)
        existing_tag = session.exec(select(Tag).where(Tag.name == tag_name_lower)).first()
        tag_objects.append(existing_tag if existing_tag else Tag(name=tag_name_lower))
    note.tags = tag_objects






    session.add(note)
    session.commit()
    session.refresh(note)
    return NoteResponse(
        id=note.id,
        title=note.title,
        content=note.content,
        category=note.category,
        tags=[tag.name for tag in note.tags],
        created_at=note.created_at,
        priority=note.priority,          
        author_email=note.author_email  
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

#Implementierung Day 6 Test: Tags ersetzen wenn sie mitgeschickt werden.

    if note_update.tags is not None:
        tag_objects = []
        seen_tags = set()
        for tag_name in note_update.tags:
            tag_name_lower = tag_name.lower().strip()
            if not tag_name_lower or tag_name_lower in seen_tags:
                continue
            seen_tags.add(tag_name_lower)
            existing_tag = session.exec(select(Tag).where(Tag.name == tag_name_lower)).first()
            tag_objects.append(existing_tag if existing_tag else Tag(name=tag_name_lower))
        note.tags = tag_objects

    session.add(note)
    session.commit()
    session.refresh(note)
    return NoteResponse(
        id=note.id,
        title=note.title,
        content=note.content,
        category=note.category,
        tags=[tag.name for tag in note.tags],
        created_at=note.created_at,
        priority=note.priority,         
        author_email=note.author_email 
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
            created_at=note.created_at,
            priority=note.priority,        
            author_email=note.author_email
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
            created_at=note.created_at,
            priority=note.priority,         
            author_email=note.author_email
        )
        for note in notes
    ]
#Gibt mir wenn ich nach dem category_name suche alle Notizen aus, die 
#den gesuchten category_name/die Kategorie x haben. Bei "work" sind das
#id1,2 und 4

#########################################
##### Statistics
#########################################


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



