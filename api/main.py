from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from api.db import SessionLocal, engine, Base
from api.models import Task
from api.schemas import TaskCreate, TaskResponse
from api.worker import process_task

app = FastAPI()

# Dependency to get DB session
def get_db():
    """
    Returns a database session.

    Yields:
        SessionLocal: The database session.

    """
    db = SessionLocal()
    print("__________Opening a new session____________")
    try:
        yield db
    finally:
        db.close()

@app.post("/tasks/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task.

    Args:
        task (TaskCreate): The task data.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        Task: The newly created task.
    """
    new_task = Task(name=task.name, status="pending")
    db.add(new_task)
    db.commit()
    # db.refresh(new_task) tells SQLAlchemy to reload the object’s data from the database, ensuring that all the fields (especially auto-generated ones) are up-to-date after a commit().
    db.refresh(new_task)

    # Send task to RabbitMQ via Celery
    process_task.delay(new_task.id)

    return new_task

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)): 
    """
    Retrieve a task by its ID.

    Args:
        task_id (int): The ID of the task to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        Task: The retrieved task.

    Raises:
        HTTPException: If the task is not found.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
