from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models
from .ai import extract_tasks
from .database import Base, engine, get_db
from .schemas import ExtractRequest, ExtractResponse


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AI Meeting Task Extractor",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://ai-task-extractor.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/extract", response_model=ExtractResponse)
def extract(
    request: ExtractRequest,
    db: Session = Depends(get_db)
):
    if not request.notes.strip():
        raise HTTPException(
            status_code=400,
            detail="Meeting notes cannot be empty"
        )

    try:
        result = extract_tasks(request.notes)

        for task in result.tasks:
            db_task = models.Task(
                title=task.title,
                assignee=task.assignee,
                due_date=task.due_date,
                status="pending"
            )

            db.add(db_task)

        db.commit()

        return result

    except Exception as error:
        db.rollback()
        print(f"Extraction error: {error}")

        raise HTTPException(
            status_code=500,
            detail="Task extraction failed"
        )