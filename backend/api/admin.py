"""
Admin API Router
Admin-only endpoints for user management, system monitoring, and maintenance
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

from backend.database import get_db, reset_database
from backend.models.user import User
from backend.models.character import Character
from backend.models.training import TrainingJob
from backend.api.auth import get_current_admin_user
from backend.config import settings

router = APIRouter(prefix="/admin", tags=["Admin"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class UserUpdateRequest(BaseModel):
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None


class SystemStatsResponse(BaseModel):
    total_users: int
    active_users: int
    total_characters: int
    total_training_jobs: int
    running_training_jobs: int


# ============================================================================
# USER MANAGEMENT
# ============================================================================

@router.get("/users", response_model=List[Dict])
def get_all_users(
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
    limit: int = 100,
    offset: int = 0
):
    """Get all users (admin only)"""

    users = db.query(User).offset(offset).limit(limit).all()

    return [user.to_dict() for user in users]


@router.get("/users/{user_id}", response_model=Dict)
def get_user_details(
    user_id: int,
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get detailed user information (admin only)"""

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Get user's characters
    characters = db.query(Character).filter(Character.user_id == user_id).all()

    # Get user's training jobs
    training_jobs = db.query(TrainingJob).filter(TrainingJob.user_id == user_id).all()

    return {
        "user": user.to_dict(),
        "characters": [char.to_dict() for char in characters],
        "training_jobs": [job.to_dict() for job in training_jobs],
    }


@router.patch("/users/{user_id}")
def update_user(
    user_id: int,
    request: UserUpdateRequest,
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update user (admin only)"""

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update fields
    if request.is_active is not None:
        user.is_active = request.is_active

    if request.is_admin is not None:
        user.is_admin = request.is_admin

    user.updated_at = datetime.utcnow()
    db.commit()

    return {"success": True, "message": "User updated", "user": user.to_dict()}


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete user (admin only)"""

    # Prevent deleting yourself
    if user_id == admin_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {"success": True, "message": f"User {user_id} deleted"}


# ============================================================================
# SYSTEM MONITORING
# ============================================================================

@router.get("/stats", response_model=SystemStatsResponse)
def get_system_stats(
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get system statistics (admin only)"""

    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    total_characters = db.query(Character).count()
    total_training_jobs = db.query(TrainingJob).count()
    running_training_jobs = db.query(TrainingJob).filter(
        TrainingJob.status == "running"
    ).count()

    return SystemStatsResponse(
        total_users=total_users,
        active_users=active_users,
        total_characters=total_characters,
        total_training_jobs=total_training_jobs,
        running_training_jobs=running_training_jobs,
    )


@router.get("/health")
def get_system_health(
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get system health status (admin only)"""

    # Check database connection
    try:
        db.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        db_status = f"error: {e}"

    return {
        "status": "healthy",
        "database": db_status,
        "version": settings.APP_VERSION,
        "debug_mode": settings.DEBUG,
        "timestamp": datetime.utcnow().isoformat(),
    }


# ============================================================================
# TRAINING MANAGEMENT
# ============================================================================

@router.get("/training/jobs")
def get_all_training_jobs(
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
    status_filter: Optional[str] = None,
    limit: int = 100
):
    """Get all training jobs across all users (admin only)"""

    query = db.query(TrainingJob)

    if status_filter:
        query = query.filter(TrainingJob.status == status_filter)

    jobs = query.order_by(TrainingJob.created_at.desc()).limit(limit).all()

    return {"jobs": [job.to_dict() for job in jobs]}


@router.post("/training/jobs/{job_id}/cancel")
def admin_cancel_training_job(
    job_id: int,
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Cancel any training job (admin only)"""

    job = db.query(TrainingJob).filter(TrainingJob.id == job_id).first()

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

    return {"success": True, "message": f"Training job {job_id} cancelled by admin"}


# ============================================================================
# DATABASE MAINTENANCE
# ============================================================================

@router.post("/database/reset")
def reset_database_admin(
    confirm: str,
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Reset database (DANGEROUS - admin only)"""

    if not settings.DEBUG:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Database reset only allowed in DEBUG mode"
        )

    if confirm != "RESET_DATABASE_CONFIRM":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid confirmation string"
        )

    # Reset database
    reset_database()

    return {
        "success": True,
        "message": "Database has been reset",
        "warning": "All data has been deleted"
    }


@router.get("/database/tables")
def get_database_tables(
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get database table information (admin only)"""

    from sqlalchemy import inspect

    inspector = inspect(db.bind)
    tables = inspector.get_table_names()

    table_info = []
    for table_name in tables:
        # Get row count
        result = db.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = result.scalar()

        table_info.append({
            "table": table_name,
            "row_count": row_count,
        })

    return {"tables": table_info}


# ============================================================================
# LOGS & DEBUGGING
# ============================================================================

@router.get("/logs/recent")
def get_recent_logs(
    admin_user: User = Depends(get_current_admin_user),
    lines: int = 100
):
    """Get recent log entries (placeholder)"""

    # TODO: Implement log reading from file
    return {
        "logs": [
            "[INFO] Example log entry 1",
            "[INFO] Example log entry 2",
            "[WARNING] Example warning",
        ][-lines:]
    }


@router.get("/config")
def get_server_config(
    admin_user: User = Depends(get_current_admin_user)
):
    """Get server configuration (admin only)"""

    return {
        "app_name": settings.APP_NAME,
        "app_version": settings.APP_VERSION,
        "debug": settings.DEBUG,
        "database_url": settings.DATABASE_URL.split("@")[-1] if "@" in settings.DATABASE_URL else "sqlite",  # Hide credentials
        "cors_origins": settings.CORS_ORIGINS,
        "training_data_dir": settings.TRAINING_DATA_DIR,
        "model_output_dir": settings.MODEL_OUTPUT_DIR,
        "whisper_model": settings.WHISPER_MODEL,
        "tts_engine": settings.TTS_ENGINE,
    }
