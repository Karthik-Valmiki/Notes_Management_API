from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.dependencies import get_db
from app.models.note import Note
from app.models.user import User
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from app.core.auth import get_current_user


router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post("/", response_model=NoteResponse)
def create_note(
    note: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    max_number = (
        db.query(func.max(Note.user_note_number))
        .filter(Note.owner_id == current_user.id)
        .scalar()
    )

    next_number = (max_number or 0) + 1

    db_note = Note(
        title=note.title,
        content=note.content,
        owner_id=current_user.id,
        user_note_number=next_number,
    )

    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return db_note


@router.get("/", response_model=list[NoteResponse])
def get_notes(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return db.query(Note).filter(Note.owner_id == current_user.id).all()


@router.get("/{user_note_number}", response_model=NoteResponse)
def get_note(
    user_note_number: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    note = (
        db.query(Note)
        .filter(
            Note.user_note_number == user_note_number, Note.owner_id == current_user.id
        )
        .first()
    )

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return note


@router.put("/{user_note_number}", response_model=NoteResponse)
def update_note(
    user_note_number: int,
    note_update: NoteUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    note = (
        db.query(Note)
        .filter(
            Note.user_note_number == user_note_number, Note.owner_id == current_user.id
        )
        .first()
    )

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if note_update.title is not None:
        note.title = note_update.title
    if note_update.content is not None:
        note.content = note_update.content

    db.commit()
    db.refresh(note)

    return note


@router.delete("/{user_note_number}")
def delete_note(
    user_note_number: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    note = (
        db.query(Note)
        .filter(
            Note.user_note_number == user_note_number, Note.owner_id == current_user.id
        )
        .first()
    )

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()

    return {"message": "Deleted"}
