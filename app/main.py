from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.db.session import engine
from app.db.base import Base
from app.models import user, note
from app.routes.note import router as note_router
from app.routes.user import router as user_router
from app.routes.admin import router as admin_router
from app.core.responses import error_response

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Notes Management API")

# --- Centralized Exception Handlers ---


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [f"{e['loc'][-1]}: {e['msg']}" for e in exc.errors()]
    return JSONResponse(status_code=422, content=error_response("; ".join(errors)))


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content=error_response(exc.detail))


# --- Routers ---

app.include_router(note_router)
app.include_router(user_router)
app.include_router(admin_router)


@app.get("/")
def root():
    return {"Notes Management API is working perfectly"}
