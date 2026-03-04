from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException

from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate


def create_note(db: Session, owner_id: int, note_data: NoteCreate) -> Note:
    max_number = (
        db.query(func.max(Note.user_note_number))
        .filter(Note.owner_id == owner_id)
        .scalar()
    )
    note = Note(
        title=note_data.title,
        content=note_data.content,
        owner_id=owner_id,
        user_note_number=(max_number or 0) + 1,
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def get_user_notes(
    db: Session,
    owner_id: int,
    page: int,
    limit: int,
    search: str | None,
) -> list[Note]:
    query = db.query(Note).filter(Note.owner_id == owner_id)
    if search:
        query = query.filter(Note.title.ilike(f"%{search}%"))
    offset = (page - 1) * limit
    return query.order_by(Note.created_at.desc()).offset(offset).limit(limit).all()


def get_note_by_number(db: Session, owner_id: int, user_note_number: int) -> Note:
    note = (
        db.query(Note)
        .filter(Note.user_note_number == user_note_number, Note.owner_id == owner_id)
        .first()
    )
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


def update_note(
    db: Session, owner_id: int, user_note_number: int, note_data: NoteUpdate
) -> Note:
    note = get_note_by_number(db, owner_id, user_note_number)
    if note_data.title is not None:
        note.title = note_data.title
    if note_data.content is not None:
        note.content = note_data.content
    db.commit()
    db.refresh(note)
    return note


def delete_note(db: Session, owner_id: int, user_note_number: int) -> None:
    note = get_note_by_number(db, owner_id, user_note_number)
    db.delete(note)
    db.commit()
