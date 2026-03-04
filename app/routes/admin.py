from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.note import Note
from app.models.user import User
from app.schemas.note import NoteResponse
from app.core.auth import get_current_admin
from app.core.responses import success_response


router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/notes", response_model=list[NoteResponse])
def get_all_notes(
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    return db.query(Note).all()


@router.delete("/notes/{note_id}")
def delete_any_note(
    note_id: int,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return success_response(message="Note deleted by admin")
