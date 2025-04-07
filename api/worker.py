from celery import Celery
import time
from .db import SessionLocal
from .models import Task

# Celery Worker (Processes Jobs)
celery = Celery("worker", # the name of this Celery instance.
    broker="pyamqp://guest@rabbitmq//", # The broker (message queue) is RabbitMQ and Uses the AMQP (Advanced Message Queuing Protocol).
    backend="rpc://" # The backend is where task results are stored.
)

@celery.task # Celery will automatically declare a queue (e.g., a default queue called celery) in RabbitMQ if it doesn’t exist
def process_task(task_id: int):
    """
    Process a task by updating its status to 'processing', simulating a long running task,
    and then updating the status to 'completed'.

    Args:
        task_id (int): The ID of the task to be processed.
    """
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.status = "processing"
        db.commit()
        time.sleep(5) # Simulate a long running task
        task.status = "completed"
        db.commit()
    db.close()
