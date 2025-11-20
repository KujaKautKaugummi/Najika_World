"""
Training API Router
Handles AI training jobs, progress tracking, and model management
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

from backend.database import get_db
from backend.models.user import User
from backend.models.training import TrainingJob, TrainingProgress
from backend.api.auth import get_current_user
from backend.config import settings

router = APIRouter(prefix="/training", tags=["Training"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class TrainingJobCreateRequest(BaseModel):
    job_name: str
    training_type: str  # "lora", "session", "code", "voice", "personality"
    description: Optional[str] = None
    config: Dict[str, Any] = {}


class TrainingJobResponse(BaseModel):
    id: int
    job_name: str
    training_type: str
    status: str
    progress: float
    created_at: str
    started_at: Optional[str]
    completed_at: Optional[str]


class TrainingProgressResponse(BaseModel):
    epoch: Optional[int]
    step: Optional[int]
    loss: Optional[float]
    accuracy: Optional[float]
    message: Optional[str]
    logged_at: str


# ============================================================================
# TRAINING JOB ENDPOINTS
# ============================================================================

@router.post("/jobs", response_model=TrainingJobResponse, status_code=status.HTTP_201_CREATED)
def create_training_job(
    request: TrainingJobCreateRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new training job"""

    # Validate training type
    valid_types = ["lora", "session", "code", "voice", "personality"]
    if request.training_type not in valid_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid training type. Must be one of: {', '.join(valid_types)}"
        )

    # Create job
    job = TrainingJob(
        user_id=current_user.id,
        job_name=request.job_name,
        training_type=request.training_type,
        description=request.description,
        config=request.config,
        status="pending",
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # Start training in background
    background_tasks.add_task(run_training_background, job.id)

    return TrainingJobResponse(
        id=job.id,
        job_name=job.job_name,
        training_type=job.training_type,
        status=job.status,
        progress=job.progress,
        created_at=job.created_at.isoformat(),
        started_at=job.started_at.isoformat() if job.started_at else None,
        completed_at=job.completed_at.isoformat() if job.completed_at else None,
    )


@router.get("/jobs", response_model=List[TrainingJobResponse])
def get_training_jobs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    status_filter: Optional[str] = None,
    limit: int = 50
):
    """Get user's training jobs"""

    query = db.query(TrainingJob).filter(TrainingJob.user_id == current_user.id)

    if status_filter:
        query = query.filter(TrainingJob.status == status_filter)

    jobs = query.order_by(TrainingJob.created_at.desc()).limit(limit).all()

    return [
        TrainingJobResponse(
            id=job.id,
            job_name=job.job_name,
            training_type=job.training_type,
            status=job.status,
            progress=job.progress,
            created_at=job.created_at.isoformat(),
            started_at=job.started_at.isoformat() if job.started_at else None,
            completed_at=job.completed_at.isoformat() if job.completed_at else None,
        )
        for job in jobs
    ]


@router.get("/jobs/{job_id}", response_model=Dict[str, Any])
def get_training_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get training job details"""

    job = db.query(TrainingJob).filter(
        TrainingJob.id == job_id,
        TrainingJob.user_id == current_user.id
    ).first()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training job not found"
        )

    return job.to_dict()


@router.post("/jobs/{job_id}/start")
def start_training_job(
    job_id: int,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a pending training job"""

    job = db.query(TrainingJob).filter(
        TrainingJob.id == job_id,
        TrainingJob.user_id == current_user.id
    ).first()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training job not found"
        )

    if job.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot start job with status: {job.status}"
        )

    # Import training launcher
    from backend.services.training_launcher import training_launcher

    # Launch training in background
    success = training_launcher.launch_training(
        job_id=job_id,
        training_type=job.training_type,
        config=job.config,
        db=db
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to launch training job"
        )

    return {"success": True, "message": "Training started in background"}


@router.post("/jobs/{job_id}/cancel")
def cancel_training_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel a running training job"""

    job = db.query(TrainingJob).filter(
        TrainingJob.id == job_id,
        TrainingJob.user_id == current_user.id
    ).first()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training job not found"
        )

    if job.status not in ["pending", "running"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot cancel job with status: {job.status}"
        )

    job.status = "cancelled"
    db.commit()

    return {"success": True, "message": "Training cancelled"}


@router.delete("/jobs/{job_id}")
def delete_training_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a training job"""

    job = db.query(TrainingJob).filter(
        TrainingJob.id == job_id,
        TrainingJob.user_id == current_user.id
    ).first()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training job not found"
        )

    if job.status == "running":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete running job. Cancel it first."
        )

    db.delete(job)
    db.commit()

    return {"success": True, "message": "Training job deleted"}


# ============================================================================
# TRAINING PROGRESS ENDPOINTS
# ============================================================================

@router.get("/jobs/{job_id}/progress", response_model=List[TrainingProgressResponse])
def get_training_progress(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 100
):
    """Get training progress logs"""

    # Verify job ownership
    job = db.query(TrainingJob).filter(
        TrainingJob.id == job_id,
        TrainingJob.user_id == current_user.id
    ).first()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training job not found"
        )

    # Get progress logs
    logs = db.query(TrainingProgress).filter(
        TrainingProgress.job_id == job_id
    ).order_by(TrainingProgress.logged_at.desc()).limit(limit).all()

    return [
        TrainingProgressResponse(
            epoch=log.epoch,
            step=log.step,
            loss=log.loss,
            accuracy=log.accuracy,
            message=log.message,
            logged_at=log.logged_at.isoformat(),
        )
        for log in logs
    ]


@router.post("/jobs/{job_id}/progress")
def add_training_progress(
    job_id: int,
    epoch: Optional[int] = None,
    step: Optional[int] = None,
    loss: Optional[float] = None,
    accuracy: Optional[float] = None,
    message: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a progress log entry (for training scripts)"""

    # Verify job ownership
    job = db.query(TrainingJob).filter(
        TrainingJob.id == job_id,
        TrainingJob.user_id == current_user.id
    ).first()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training job not found"
        )

    # Create progress entry
    progress = TrainingProgress(
        job_id=job_id,
        epoch=epoch,
        step=step,
        loss=loss,
        accuracy=accuracy,
        message=message,
    )

    db.add(progress)

    # Update job progress
    if epoch and job.config.get("num_epochs"):
        job.progress = (epoch / job.config["num_epochs"]) * 100

    db.commit()

    return {"success": True, "message": "Progress logged"}


# ============================================================================
# TRAINING STATISTICS
# ============================================================================

@router.get("/stats")
def get_training_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get training statistics for user"""

    total_jobs = db.query(TrainingJob).filter(TrainingJob.user_id == current_user.id).count()
    completed_jobs = db.query(TrainingJob).filter(
        TrainingJob.user_id == current_user.id,
        TrainingJob.status == "completed"
    ).count()
    running_jobs = db.query(TrainingJob).filter(
        TrainingJob.user_id == current_user.id,
        TrainingJob.status == "running"
    ).count()
    failed_jobs = db.query(TrainingJob).filter(
        TrainingJob.user_id == current_user.id,
        TrainingJob.status == "failed"
    ).count()

    return {
        "total_jobs": total_jobs,
        "completed": completed_jobs,
        "running": running_jobs,
        "failed": failed_jobs,
        "pending": total_jobs - completed_jobs - running_jobs - failed_jobs,
    }


# ============================================================================
# BACKGROUND TRAINING FUNCTIONS
# ============================================================================

def run_training_background(job_id: int):
    """
    Background task wrapper to run training
    Creates a new event loop for the async training function
    """
    import asyncio

    # Create new event loop for background task
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(run_training_async(job_id))
    except Exception as e:
        logger.error(f"Training job {job_id} failed: {e}", exc_info=True)
    finally:
        loop.close()


async def run_training_async(job_id: int):
    """
    Async training execution
    This integrates with existing training scripts:
    - najika_lora_training.py
    - NAJIKA_SESSION_TRAINING.py
    - NAJIKA_CODE_TRAINING.py
    - etc.
    """
    from backend.database import SessionLocal

    db = SessionLocal()

    try:
        # Get job
        job = db.query(TrainingJob).filter(TrainingJob.id == job_id).first()

        if not job:
            logger.error(f"Training job {job_id} not found")
            return

        # Update status to running
        job.status = "running"
        job.started_at = datetime.utcnow()
        db.commit()

        logger.info(f"Starting training job {job_id}: {job.job_name} ({job.training_type})")

        # Execute training based on type
        if job.training_type == "lora":
            await train_lora(job, db)
        elif job.training_type == "session":
            await train_session(job, db)
        elif job.training_type == "code":
            await train_code(job, db)
        elif job.training_type == "voice":
            await train_voice(job, db)
        elif job.training_type == "personality":
            await train_personality(job, db)
        else:
            raise ValueError(f"Unknown training type: {job.training_type}")

        # Mark as completed
        job.status = "completed"
        job.completed_at = datetime.utcnow()
        job.progress = 100.0
        db.commit()

        logger.info(f"Training job {job_id} completed successfully")

    except Exception as e:
        logger.error(f"Training job {job_id} failed: {e}", exc_info=True)

        # Mark as failed
        job.status = "failed"
        job.error_message = str(e)
        db.commit()

    finally:
        db.close()


# ============================================================================
# TRAINING TYPE IMPLEMENTATIONS
# ============================================================================

async def train_lora(job: TrainingJob, db: Session):
    """
    LoRA training implementation
    Integrates with najika_lora_training.py
    """
    import asyncio

    config = job.config
    num_epochs = config.get("num_epochs", 10)

    for epoch in range(1, num_epochs + 1):
        # Simulate training step
        await asyncio.sleep(2)  # Simulate work

        # Log progress
        progress = TrainingProgress(
            job_id=job.id,
            epoch=epoch,
            step=epoch * 100,
            loss=1.0 / (epoch + 1),  # Simulated loss decrease
            message=f"Epoch {epoch}/{num_epochs} completed"
        )
        db.add(progress)

        # Update job progress
        job.progress = (epoch / num_epochs) * 100
        db.commit()

        logger.info(f"Job {job.id}: Epoch {epoch}/{num_epochs} - Loss: {progress.loss:.4f}")


async def train_session(job: TrainingJob, db: Session):
    """
    Session training implementation
    Integrates with NAJIKA_SESSION_TRAINING.py
    """
    import asyncio

    config = job.config
    num_steps = config.get("num_steps", 100)

    for step in range(1, num_steps + 1):
        await asyncio.sleep(0.5)  # Simulate work

        if step % 10 == 0:
            # Log progress every 10 steps
            progress = TrainingProgress(
                job_id=job.id,
                step=step,
                message=f"Session training step {step}/{num_steps}"
            )
            db.add(progress)

            job.progress = (step / num_steps) * 100
            db.commit()


async def train_code(job: TrainingJob, db: Session):
    """
    Code training implementation
    Integrates with NAJIKA_CODE_TRAINING.py
    """
    import asyncio

    config = job.config
    num_iterations = config.get("num_iterations", 50)

    for iteration in range(1, num_iterations + 1):
        await asyncio.sleep(1)

        if iteration % 5 == 0:
            progress = TrainingProgress(
                job_id=job.id,
                step=iteration,
                accuracy=0.5 + (iteration / num_iterations) * 0.4,  # Simulated accuracy increase
                message=f"Code training iteration {iteration}/{num_iterations}"
            )
            db.add(progress)

            job.progress = (iteration / num_iterations) * 100
            db.commit()


async def train_voice(job: TrainingJob, db: Session):
    """
    Voice training implementation
    For voice cloning and TTS fine-tuning
    """
    import asyncio

    config = job.config
    num_epochs = config.get("num_epochs", 20)

    for epoch in range(1, num_epochs + 1):
        await asyncio.sleep(3)  # Voice training is slower

        progress = TrainingProgress(
            job_id=job.id,
            epoch=epoch,
            message=f"Voice training epoch {epoch}/{num_epochs}"
        )
        db.add(progress)

        job.progress = (epoch / num_epochs) * 100
        db.commit()


async def train_personality(job: TrainingJob, db: Session):
    """
    Personality training implementation
    For fine-tuning AI personality traits
    """
    import asyncio

    config = job.config
    num_batches = config.get("num_batches", 30)

    for batch in range(1, num_batches + 1):
        await asyncio.sleep(1.5)

        progress = TrainingProgress(
            job_id=job.id,
            step=batch,
            message=f"Personality training batch {batch}/{num_batches}"
        )
        db.add(progress)

        job.progress = (batch / num_batches) * 100
        db.commit()
