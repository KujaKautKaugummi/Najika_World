"""
Unified Training Interface
Single entry point for all training operations
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from sqlalchemy.orm import Session

from backend.models.training import TrainingJob, TrainingProgress
from backend.services.training_launcher import TrainingLauncher
from backend.services.training_scheduler import get_scheduler, TrainingPriority
from backend.services.training_progress_tracker import get_progress_tracker
from backend.config import settings


class UnifiedTrainingInterface:
    """
    Unified Training Interface

    Single interface for all training operations:
    - Create training jobs
    - Launch training (immediate or scheduled)
    - Track progress
    - Manage training queue
    - Get training results
    """

    def __init__(self):
        self.launcher = TrainingLauncher()
        self.scheduler = get_scheduler()
        self.progress_tracker = get_progress_tracker()

    # ============================================================================
    # JOB CREATION
    # ============================================================================

    def create_lora_training(
        self,
        db: Session,
        user_id: int,
        job_name: str,
        dataset_path: str,
        num_epochs: int = 3,
        learning_rate: float = 0.0002,
        batch_size: int = 4,
        max_length: int = 2048,
        lora_r: int = 8,
        lora_alpha: int = 16,
        priority: TrainingPriority = TrainingPriority.NORMAL,
        scheduled_time: Optional[datetime] = None
    ) -> TrainingJob:
        """
        Create LoRA training job

        Args:
            db: Database session
            user_id: User ID
            job_name: Job name
            dataset_path: Path to training dataset
            num_epochs: Number of training epochs
            learning_rate: Learning rate
            batch_size: Batch size
            max_length: Max sequence length
            lora_r: LoRA r parameter
            lora_alpha: LoRA alpha parameter
            priority: Job priority
            scheduled_time: When to start (None = immediate)

        Returns:
            Created TrainingJob
        """

        config = {
            "dataset_path": dataset_path,
            "num_epochs": num_epochs,
            "learning_rate": learning_rate,
            "batch_size": batch_size,
            "max_length": max_length,
            "lora_r": lora_r,
            "lora_alpha": lora_alpha
        }

        return self._create_job(
            db=db,
            user_id=user_id,
            job_name=job_name,
            training_type="lora",
            config=config,
            priority=priority,
            scheduled_time=scheduled_time
        )

    def create_session_training(
        self,
        db: Session,
        user_id: int,
        job_name: str,
        session_file: str,
        priority: TrainingPriority = TrainingPriority.NORMAL,
        scheduled_time: Optional[datetime] = None
    ) -> TrainingJob:
        """Create session training job"""

        config = {
            "session_file": session_file
        }

        return self._create_job(
            db=db,
            user_id=user_id,
            job_name=job_name,
            training_type="session",
            config=config,
            priority=priority,
            scheduled_time=scheduled_time
        )

    def create_code_training(
        self,
        db: Session,
        user_id: int,
        job_name: str,
        code_directory: str,
        file_extensions: List[str] = [".py", ".js", ".cpp"],
        priority: TrainingPriority = TrainingPriority.NORMAL,
        scheduled_time: Optional[datetime] = None
    ) -> TrainingJob:
        """Create code training job"""

        config = {
            "code_directory": code_directory,
            "file_extensions": file_extensions
        }

        return self._create_job(
            db=db,
            user_id=user_id,
            job_name=job_name,
            training_type="code",
            config=config,
            priority=priority,
            scheduled_time=scheduled_time
        )

    def create_voice_training(
        self,
        db: Session,
        user_id: int,
        job_name: str,
        video_file: str,
        priority: TrainingPriority = TrainingPriority.NORMAL,
        scheduled_time: Optional[datetime] = None
    ) -> TrainingJob:
        """Create voice training job"""

        config = {
            "video_file": video_file
        }

        return self._create_job(
            db=db,
            user_id=user_id,
            job_name=job_name,
            training_type="voice",
            config=config,
            priority=priority,
            scheduled_time=scheduled_time
        )

    def create_personality_training(
        self,
        db: Session,
        user_id: int,
        job_name: str,
        personality_data: Dict[str, Any],
        priority: TrainingPriority = TrainingPriority.NORMAL,
        scheduled_time: Optional[datetime] = None
    ) -> TrainingJob:
        """Create personality training job"""

        config = {
            "personality_data": personality_data
        }

        return self._create_job(
            db=db,
            user_id=user_id,
            job_name=job_name,
            training_type="personality",
            config=config,
            priority=priority,
            scheduled_time=scheduled_time
        )

    def _create_job(
        self,
        db: Session,
        user_id: int,
        job_name: str,
        training_type: str,
        config: Dict[str, Any],
        priority: TrainingPriority,
        scheduled_time: Optional[datetime]
    ) -> TrainingJob:
        """Internal method to create a training job"""

        # Create database record
        job = TrainingJob(
            user_id=user_id,
            job_name=job_name,
            training_type=training_type,
            status="queued" if not scheduled_time else "scheduled",
            config=config,
            created_at=datetime.now()
        )

        db.add(job)
        db.commit()
        db.refresh(job)

        # Add to scheduler
        self.scheduler.add_job(
            job_id=job.id,
            training_type=training_type,
            config=config,
            priority=priority,
            scheduled_time=scheduled_time
        )

        print(f"✅ Training job created: {job.id} ({training_type})")

        return job

    # ============================================================================
    # JOB MANAGEMENT
    # ============================================================================

    def cancel_job(self, db: Session, job_id: int) -> bool:
        """Cancel a training job"""

        job = db.query(TrainingJob).filter(TrainingJob.id == job_id).first()
        if not job:
            return False

        # Cancel in scheduler
        self.scheduler.cancel_job(job_id)

        # Update database
        job.status = "cancelled"
        job.completed_at = datetime.now()
        db.commit()

        print(f"❌ Job {job_id} cancelled")
        return True

    def get_job_status(self, db: Session, job_id: int) -> Dict[str, Any]:
        """Get comprehensive job status"""

        # Get from database
        job = db.query(TrainingJob).filter(TrainingJob.id == job_id).first()
        if not job:
            return {"error": "Job not found"}

        # Get from scheduler
        scheduler_status = self.scheduler.get_job_status(job_id)

        # Get from progress tracker
        progress = self.progress_tracker.get_current_progress(job_id)

        return {
            "job_id": job.id,
            "job_name": job.job_name,
            "training_type": job.training_type,
            "status": job.status,
            "created_at": job.created_at.isoformat(),
            "started_at": job.started_at.isoformat() if job.started_at else None,
            "completed_at": job.completed_at.isoformat() if job.completed_at else None,
            "config": job.config,
            "scheduler_status": scheduler_status,
            "progress": progress
        }

    def get_all_jobs(
        self,
        db: Session,
        user_id: Optional[int] = None,
        status_filter: Optional[str] = None,
        training_type_filter: Optional[str] = None,
        limit: int = 50
    ) -> List[TrainingJob]:
        """Get all training jobs with filters"""

        query = db.query(TrainingJob)

        if user_id:
            query = query.filter(TrainingJob.user_id == user_id)

        if status_filter:
            query = query.filter(TrainingJob.status == status_filter)

        if training_type_filter:
            query = query.filter(TrainingJob.training_type == training_type_filter)

        jobs = query.order_by(TrainingJob.created_at.desc()).limit(limit).all()

        return jobs

    def get_queue_status(self) -> Dict[str, Any]:
        """Get training queue status"""
        return self.scheduler.get_queue_status()

    # ============================================================================
    # PROGRESS TRACKING
    # ============================================================================

    def get_job_progress(self, job_id: int) -> Optional[Dict[str, Any]]:
        """Get current progress for a job"""
        return self.progress_tracker.get_current_progress(job_id)

    def get_progress_history(self, job_id: int, last_n: Optional[int] = None) -> List[Dict]:
        """Get progress history for a job"""
        return self.progress_tracker.get_progress_history(job_id, last_n=last_n)

    def get_training_summary(self, job_id: int) -> Dict[str, Any]:
        """Get training summary statistics"""
        return self.progress_tracker.get_summary_statistics(job_id)

    # ============================================================================
    # RECURRING JOBS
    # ============================================================================

    def create_recurring_training(
        self,
        db: Session,
        user_id: int,
        job_name: str,
        training_type: str,
        config: Dict[str, Any],
        interval_hours: int,
        priority: TrainingPriority = TrainingPriority.LOW
    ) -> int:
        """Create a recurring training job"""

        # Create base job ID
        base_job_id = int(f"9{user_id}{int(datetime.now().timestamp())}")

        # Add to scheduler
        self.scheduler.add_recurring_job(
            job_id=base_job_id,
            training_type=training_type,
            config=config,
            interval_hours=interval_hours,
            priority=priority
        )

        print(f"🔄 Recurring job created: {base_job_id} (every {interval_hours}h)")

        return base_job_id

    # ============================================================================
    # UTILITIES
    # ============================================================================

    def cleanup_old_jobs(self, db: Session, max_age_days: int = 30):
        """Clean up old completed jobs"""

        cutoff_date = datetime.now() - timedelta(days=max_age_days)

        # Delete old jobs from database
        deleted_count = db.query(TrainingJob).filter(
            TrainingJob.status.in_(["completed", "failed", "cancelled"]),
            TrainingJob.completed_at < cutoff_date
        ).delete()

        db.commit()

        # Cleanup progress tracker
        self.progress_tracker.cleanup_old_jobs(max_age_hours=max_age_days * 24)

        print(f"🗑️ Cleaned up {deleted_count} old jobs")

        return deleted_count


# Global unified interface instance
_unified_training = None


def get_training_interface() -> UnifiedTrainingInterface:
    """Get global unified training interface"""
    global _unified_training
    if _unified_training is None:
        _unified_training = UnifiedTrainingInterface()
    return _unified_training


if __name__ == "__main__":
    # Test usage
    print("🧪 Testing Unified Training Interface\n")

    interface = UnifiedTrainingInterface()

    # Example: Create a LoRA training job
    from backend.database import SessionLocal
    db = SessionLocal()

    job = interface.create_lora_training(
        db=db,
        user_id=1,
        job_name="Test LoRA Training",
        dataset_path="./training_data/test.jsonl",
        num_epochs=3,
        priority=TrainingPriority.HIGH
    )

    print(f"\nCreated job: {job.id}")
    print(f"Status: {job.status}")

    # Get queue status
    queue_status = interface.get_queue_status()
    print(f"\nQueue status: {queue_status}")

    db.close()
