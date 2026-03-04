from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.user import User
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from app.core.auth import get_current_user
from app.core.responses import success_response
from app.services import note_service


router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post("/", response_model=NoteResponse, status_code=201)
def create_note(
    note: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return note_service.create_note(db, current_user.id, note)


@router.get("/", response_model=list[NoteResponse])
def get_notes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Results per page"),
    search: str | None = Query(None, description="Search by title keyword"),
):
    return note_service.get_user_notes(db, current_user.id, page, limit, search)


@router.get("/{user_note_number}", response_model=NoteResponse)
def get_note(
    user_note_number: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return note_service.get_note_by_number(db, current_user.id, user_note_number)


@router.put("/{user_note_number}", response_model=NoteResponse)
def update_note(
    user_note_number: int,
    note_update: NoteUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return note_service.update_note(db, current_user.id, user_note_number, note_update)


@router.delete("/{user_note_number}")
def delete_note(
    user_note_number: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    note_service.delete_note(db, current_user.id, user_note_number)
    return success_response(message="Note deleted successfully")
