"""
Training Scheduler Service
Manages scheduled training jobs, queues, and automatic training
"""

import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from queue import Queue, PriorityQueue
from dataclasses import dataclass, field
from enum import Enum
from sqlalchemy.orm import Session

from backend.models.training import TrainingJob, TrainingProgress
from backend.services.training_launcher import TrainingLauncher
from backend.config import settings


class TrainingPriority(Enum):
    """Training job priority levels"""
    LOW = 3
    NORMAL = 2
    HIGH = 1
    CRITICAL = 0


@dataclass(order=True)
class ScheduledTrainingJob:
    """Scheduled training job with priority"""
    priority: int
    job_id: int = field(compare=False)
    scheduled_time: datetime = field(compare=False)
    training_type: str = field(compare=False)
    config: Dict[str, Any] = field(compare=False)


class TrainingScheduler:
    """
    Training Scheduler Service

    Features:
    - Job queue with priority
    - Scheduled training (future jobs)
    - Automatic recurring training
    - Resource management (max concurrent jobs)
    - Job cancellation
    - Progress tracking
    """

    def __init__(self, max_concurrent_jobs: int = 2):
        self.max_concurrent_jobs = max_concurrent_jobs
        self.launcher = TrainingLauncher()

        # Job queues
        self.job_queue = PriorityQueue()
        self.scheduled_jobs = []  # Jobs with future start time
        self.running_jobs = {}  # {job_id: thread}
        self.recurring_jobs = {}  # {job_id: config}

        # State
        self.running = False
        self.scheduler_thread = None

        # Statistics
        self.stats = {
            "total_jobs_processed": 0,
            "successful_jobs": 0,
            "failed_jobs": 0,
            "cancelled_jobs": 0,
            "total_training_time": 0
        }

    def start(self):
        """Start the scheduler"""
        if self.running:
            print("⚠️ Scheduler already running")
            return

        self.running = True
        self.scheduler_thread = threading.Thread(
            target=self._scheduler_loop,
            daemon=True
        )
        self.scheduler_thread.start()
        print("✅ Training Scheduler started")

    def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        print("🛑 Training Scheduler stopped")

    def add_job(
        self,
        job_id: int,
        training_type: str,
        config: Dict[str, Any],
        priority: TrainingPriority = TrainingPriority.NORMAL,
        scheduled_time: Optional[datetime] = None
    ):
        """
        Add a training job to the queue

        Args:
            job_id: Training job ID
            training_type: Type of training
            config: Training configuration
            priority: Job priority
            scheduled_time: If set, job will start at this time (future)
        """

        if scheduled_time and scheduled_time > datetime.now():
            # Schedule for future execution
            self.scheduled_jobs.append(
                ScheduledTrainingJob(
                    priority=priority.value,
                    job_id=job_id,
                    scheduled_time=scheduled_time,
                    training_type=training_type,
                    config=config
                )
            )
            print(f"📅 Job {job_id} scheduled for {scheduled_time}")
        else:
            # Add to immediate queue
            self.job_queue.put(
                ScheduledTrainingJob(
                    priority=priority.value,
                    job_id=job_id,
                    scheduled_time=datetime.now(),
                    training_type=training_type,
                    config=config
                )
            )
            print(f"📥 Job {job_id} added to queue (priority: {priority.name})")

    def add_recurring_job(
        self,
        job_id: int,
        training_type: str,
        config: Dict[str, Any],
        interval_hours: int,
        priority: TrainingPriority = TrainingPriority.LOW
    ):
        """
        Add a recurring training job

        Args:
            job_id: Base job ID (will be incremented for each run)
            training_type: Type of training
            config: Training configuration
            interval_hours: Hours between executions
            priority: Job priority
        """

        self.recurring_jobs[job_id] = {
            "training_type": training_type,
            "config": config,
            "interval_hours": interval_hours,
            "priority": priority,
            "last_run": None,
            "next_run": datetime.now()
        }

        print(f"🔄 Recurring job {job_id} added (every {interval_hours}h)")

    def cancel_job(self, job_id: int):
        """Cancel a job (running, queued, or scheduled)"""

        # Remove from queue (hard to do with PriorityQueue, skip for now)
        # Remove from scheduled jobs
        self.scheduled_jobs = [
            job for job in self.scheduled_jobs
            if job.job_id != job_id
        ]

        # Cancel running job
        if job_id in self.running_jobs:
            # In a real implementation, we'd need to send a signal to the thread
            # For now, just remove from tracking
            del self.running_jobs[job_id]
            self.stats["cancelled_jobs"] += 1
            print(f"❌ Job {job_id} cancelled")
            return True

        return False

    def _scheduler_loop(self):
        """Main scheduler loop"""

        while self.running:
            # 1. Check scheduled jobs
            self._process_scheduled_jobs()

            # 2. Check recurring jobs
            self._process_recurring_jobs()

            # 3. Process job queue
            self._process_job_queue()

            # Sleep to avoid busy-waiting
            time.sleep(5)

    def _process_scheduled_jobs(self):
        """Move scheduled jobs to queue if their time has come"""

        now = datetime.now()
        ready_jobs = []

        for job in self.scheduled_jobs:
            if job.scheduled_time <= now:
                ready_jobs.append(job)

        for job in ready_jobs:
            self.scheduled_jobs.remove(job)
            self.job_queue.put(job)
            print(f"⏰ Scheduled job {job.job_id} moved to queue")

    def _process_recurring_jobs(self):
        """Check if any recurring jobs need to run"""

        now = datetime.now()

        for job_id, config in self.recurring_jobs.items():
            if config["next_run"] <= now:
                # Create new job with incremented ID
                new_job_id = int(f"{job_id}{int(time.time())}")

                self.add_job(
                    job_id=new_job_id,
                    training_type=config["training_type"],
                    config=config["config"],
                    priority=config["priority"]
                )

                # Update next run time
                config["last_run"] = now
                config["next_run"] = now + timedelta(hours=config["interval_hours"])

                print(f"🔄 Recurring job {job_id} triggered (next: {config['next_run']})")

    def _process_job_queue(self):
        """Process jobs from the queue"""

        # Check if we can start a new job
        if len(self.running_jobs) >= self.max_concurrent_jobs:
            return

        if self.job_queue.empty():
            return

        # Get next job from queue
        job = self.job_queue.get()

        # Launch the job
        from backend.database import SessionLocal
        db = SessionLocal()

        success = self.launcher.launch_training(
            job_id=job.job_id,
            training_type=job.training_type,
            config=job.config,
            db=db,
            on_progress=self._on_job_progress
        )

        db.close()

        if success:
            # Track as running
            self.running_jobs[job.job_id] = {
                "start_time": datetime.now(),
                "training_type": job.training_type
            }
            print(f"▶️ Job {job.job_id} started ({job.training_type})")
        else:
            self.stats["failed_jobs"] += 1

    def _on_job_progress(self, job_id: int, progress: Dict[str, Any]):
        """Callback for job progress updates"""

        # Check if job completed
        if progress.get("status") == "completed":
            self._on_job_completed(job_id, success=True)
        elif progress.get("status") == "failed":
            self._on_job_completed(job_id, success=False)

    def _on_job_completed(self, job_id: int, success: bool):
        """Handle job completion"""

        if job_id in self.running_jobs:
            job_info = self.running_jobs[job_id]
            duration = (datetime.now() - job_info["start_time"]).total_seconds()

            del self.running_jobs[job_id]

            # Update stats
            self.stats["total_jobs_processed"] += 1
            self.stats["total_training_time"] += duration

            if success:
                self.stats["successful_jobs"] += 1
                print(f"✅ Job {job_id} completed (duration: {duration:.1f}s)")
            else:
                self.stats["failed_jobs"] += 1
                print(f"❌ Job {job_id} failed (duration: {duration:.1f}s)")

    def get_queue_status(self) -> Dict[str, Any]:
        """Get current queue status"""

        return {
            "running_jobs": len(self.running_jobs),
            "queued_jobs": self.job_queue.qsize(),
            "scheduled_jobs": len(self.scheduled_jobs),
            "recurring_jobs": len(self.recurring_jobs),
            "max_concurrent": self.max_concurrent_jobs,
            "stats": self.stats,
            "running_job_ids": list(self.running_jobs.keys())
        }

    def get_job_status(self, job_id: int) -> Dict[str, Any]:
        """Get status of a specific job"""

        # Check if running
        if job_id in self.running_jobs:
            job_info = self.running_jobs[job_id]
            duration = (datetime.now() - job_info["start_time"]).total_seconds()
            return {
                "status": "running",
                "training_type": job_info["training_type"],
                "duration_seconds": duration
            }

        # Check if scheduled
        for job in self.scheduled_jobs:
            if job.job_id == job_id:
                return {
                    "status": "scheduled",
                    "scheduled_time": job.scheduled_time.isoformat(),
                    "training_type": job.training_type
                }

        return {
            "status": "not_found"
        }


# Global scheduler instance
_scheduler_instance = None


def get_scheduler() -> TrainingScheduler:
    """Get global scheduler instance"""
    global _scheduler_instance
    if _scheduler_instance is None:
        _scheduler_instance = TrainingScheduler(
            max_concurrent_jobs=getattr(settings, 'MAX_CONCURRENT_TRAINING_JOBS', 2)
        )
        _scheduler_instance.start()
    return _scheduler_instance


if __name__ == "__main__":
    # Test scheduler
    scheduler = TrainingScheduler(max_concurrent_jobs=1)
    scheduler.start()

    # Add some test jobs
    scheduler.add_job(
        job_id=1,
        training_type="lora",
        config={"epochs": 3},
        priority=TrainingPriority.HIGH
    )

    scheduler.add_job(
        job_id=2,
        training_type="session",
        config={},
        priority=TrainingPriority.NORMAL
    )

    # Add recurring job
    scheduler.add_recurring_job(
        job_id=100,
        training_type="personality",
        config={},
        interval_hours=24,
        priority=TrainingPriority.LOW
    )

    print("\n📊 Queue Status:")
    print(scheduler.get_queue_status())

    # Keep running
    try:
        while True:
            time.sleep(10)
            print("\n📊 Queue Status:")
            print(scheduler.get_queue_status())
    except KeyboardInterrupt:
        scheduler.stop()
