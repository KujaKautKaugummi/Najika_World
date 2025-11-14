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

    # TODO: Start training in background
    # background_tasks.add_task(run_training, job.id, db)

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

    job.status = "running"
    job.started_at = datetime.utcnow()
    db.commit()

    # TODO: Start actual training
    # background_tasks.add_task(run_training, job_id, db)

    return {"success": True, "message": "Training started"}


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
# HELPER FUNCTIONS (to be implemented)
# ============================================================================

def run_training(job_id: int, db: Session):
    """
    Background task to run training
    This should integrate with existing training scripts:
    - najika_lora_training.py
    - NAJIKA_SESSION_TRAINING.py
    - NAJIKA_CODE_TRAINING.py
    - etc.
    """
    # TODO: Implement actual training logic
    pass
