from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.models import user, note
from app.routes.note import router as note_router
from app.routes.user import router as user_router
from app.routes.admin import router as admin_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(note_router)
app.include_router(user_router)
app.include_router(admin_router)


@app.get("/")
def root():
    return {"message": "API Running"}
