"""
Training Progress Tracker
Real-time progress tracking for all training jobs
"""

import time
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from collections import defaultdict
from sqlalchemy.orm import Session

from backend.models.training import TrainingJob, TrainingProgress
from backend.config import settings


@dataclass
class TrainingMetrics:
    """Training metrics snapshot"""
    timestamp: str
    epoch: int
    step: int
    loss: float
    accuracy: Optional[float] = None
    learning_rate: Optional[float] = None
    gpu_memory_mb: Optional[int] = None
    samples_per_second: Optional[float] = None
    estimated_time_remaining: Optional[int] = None


class TrainingProgressTracker:
    """
    Real-time training progress tracker

    Features:
    - Track training metrics (loss, accuracy, etc.)
    - Calculate estimated time remaining
    - Store progress snapshots
    - Notify listeners on progress updates
    - Export progress history
    """

    def __init__(self):
        # Progress data: {job_id: [TrainingMetrics]}
        self.progress_history = defaultdict(list)

        # Current progress: {job_id: TrainingMetrics}
        self.current_progress = {}

        # Listeners: {job_id: [callbacks]}
        self.listeners = defaultdict(list)

        # Job metadata
        self.job_metadata = {}

    def start_tracking(
        self,
        job_id: int,
        total_epochs: int,
        total_steps: int,
        training_type: str
    ):
        """
        Start tracking a training job

        Args:
            job_id: Training job ID
            total_epochs: Total number of epochs
            total_steps: Total number of steps
            training_type: Type of training
        """

        self.job_metadata[job_id] = {
            "total_epochs": total_epochs,
            "total_steps": total_steps,
            "training_type": training_type,
            "start_time": datetime.now(),
            "status": "running"
        }

        print(f"📊 Started tracking job {job_id} ({training_type})")

    def update_progress(
        self,
        job_id: int,
        epoch: int,
        step: int,
        loss: float,
        accuracy: Optional[float] = None,
        learning_rate: Optional[float] = None,
        gpu_memory_mb: Optional[int] = None,
        samples_per_second: Optional[float] = None
    ):
        """
        Update training progress

        Args:
            job_id: Training job ID
            epoch: Current epoch
            step: Current step
            loss: Training loss
            accuracy: Training accuracy (optional)
            learning_rate: Current learning rate (optional)
            gpu_memory_mb: GPU memory usage in MB (optional)
            samples_per_second: Training speed (optional)
        """

        # Calculate estimated time remaining
        eta = self._calculate_eta(job_id, epoch, step)

        # Create metrics snapshot
        metrics = TrainingMetrics(
            timestamp=datetime.now().isoformat(),
            epoch=epoch,
            step=step,
            loss=loss,
            accuracy=accuracy,
            learning_rate=learning_rate,
            gpu_memory_mb=gpu_memory_mb,
            samples_per_second=samples_per_second,
            estimated_time_remaining=eta
        )

        # Store progress
        self.progress_history[job_id].append(metrics)
        self.current_progress[job_id] = metrics

        # Notify listeners
        self._notify_listeners(job_id, metrics)

    def _calculate_eta(self, job_id: int, current_epoch: int, current_step: int) -> Optional[int]:
        """Calculate estimated time remaining in seconds"""

        if job_id not in self.job_metadata:
            return None

        metadata = self.job_metadata[job_id]
        history = self.progress_history[job_id]

        if len(history) < 2:
            return None

        # Calculate progress percentage
        total_epochs = metadata["total_epochs"]
        total_steps = metadata["total_steps"]

        if total_epochs == 0:
            return None

        progress = (current_epoch + (current_step / total_steps)) / total_epochs

        if progress == 0:
            return None

        # Calculate elapsed time
        elapsed = (datetime.now() - metadata["start_time"]).total_seconds()

        # Estimate total time
        estimated_total = elapsed / progress

        # ETA = estimated_total - elapsed
        eta = int(estimated_total - elapsed)

        return max(0, eta)

    def add_listener(self, job_id: int, callback: Callable[[TrainingMetrics], None]):
        """
        Add a progress listener

        Args:
            job_id: Training job ID
            callback: Function to call on progress update
        """
        self.listeners[job_id].append(callback)

    def remove_listener(self, job_id: int, callback: Callable):
        """Remove a progress listener"""
        if job_id in self.listeners:
            self.listeners[job_id] = [
                cb for cb in self.listeners[job_id]
                if cb != callback
            ]

    def _notify_listeners(self, job_id: int, metrics: TrainingMetrics):
        """Notify all listeners for this job"""
        for callback in self.listeners[job_id]:
            try:
                callback(metrics)
            except Exception as e:
                print(f"⚠️ Listener error for job {job_id}: {e}")

    def get_current_progress(self, job_id: int) -> Optional[Dict[str, Any]]:
        """Get current progress for a job"""

        if job_id not in self.current_progress:
            return None

        metrics = self.current_progress[job_id]
        metadata = self.job_metadata.get(job_id, {})

        return {
            "job_id": job_id,
            "status": metadata.get("status", "unknown"),
            "training_type": metadata.get("training_type", "unknown"),
            "current_metrics": asdict(metrics),
            "total_epochs": metadata.get("total_epochs", 0),
            "total_steps": metadata.get("total_steps", 0),
            "progress_percentage": self._calculate_progress_percentage(job_id, metrics),
            "start_time": metadata.get("start_time").isoformat() if metadata.get("start_time") else None
        }

    def _calculate_progress_percentage(self, job_id: int, metrics: TrainingMetrics) -> float:
        """Calculate overall progress percentage"""

        if job_id not in self.job_metadata:
            return 0.0

        metadata = self.job_metadata[job_id]
        total_epochs = metadata["total_epochs"]
        total_steps = metadata["total_steps"]

        if total_epochs == 0:
            return 0.0

        progress = (metrics.epoch + (metrics.step / total_steps)) / total_epochs
        return min(100.0, progress * 100.0)

    def get_progress_history(self, job_id: int, last_n: Optional[int] = None) -> List[Dict]:
        """
        Get progress history for a job

        Args:
            job_id: Training job ID
            last_n: Return only last N snapshots (None = all)

        Returns:
            List of metrics snapshots
        """

        history = self.progress_history[job_id]

        if last_n:
            history = history[-last_n:]

        return [asdict(metrics) for metrics in history]

    def mark_completed(self, job_id: int, success: bool = True):
        """Mark a job as completed"""

        if job_id in self.job_metadata:
            self.job_metadata[job_id]["status"] = "completed" if success else "failed"
            self.job_metadata[job_id]["end_time"] = datetime.now()

            # Calculate total duration
            duration = (
                self.job_metadata[job_id]["end_time"] -
                self.job_metadata[job_id]["start_time"]
            ).total_seconds()

            self.job_metadata[job_id]["duration_seconds"] = duration

            status = "✅ completed" if success else "❌ failed"
            print(f"📊 Job {job_id} {status} (duration: {duration:.1f}s)")

    def export_progress(self, job_id: int, filepath: str):
        """Export progress history to JSON file"""

        data = {
            "job_id": job_id,
            "metadata": self.job_metadata.get(job_id, {}),
            "history": self.get_progress_history(job_id)
        }

        # Convert datetime objects to strings
        if "start_time" in data["metadata"]:
            data["metadata"]["start_time"] = data["metadata"]["start_time"].isoformat()
        if "end_time" in data["metadata"]:
            data["metadata"]["end_time"] = data["metadata"]["end_time"].isoformat()

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"💾 Progress exported to {filepath}")

    def get_summary_statistics(self, job_id: int) -> Dict[str, Any]:
        """Get summary statistics for a job"""

        if job_id not in self.progress_history:
            return {}

        history = self.progress_history[job_id]
        metadata = self.job_metadata.get(job_id, {})

        if not history:
            return {}

        losses = [m.loss for m in history]
        accuracies = [m.accuracy for m in history if m.accuracy is not None]

        return {
            "job_id": job_id,
            "training_type": metadata.get("training_type", "unknown"),
            "status": metadata.get("status", "unknown"),
            "total_snapshots": len(history),
            "total_epochs": metadata.get("total_epochs", 0),
            "total_steps": metadata.get("total_steps", 0),
            "duration_seconds": metadata.get("duration_seconds"),
            "loss": {
                "initial": losses[0] if losses else None,
                "final": losses[-1] if losses else None,
                "min": min(losses) if losses else None,
                "max": max(losses) if losses else None,
                "average": sum(losses) / len(losses) if losses else None
            },
            "accuracy": {
                "initial": accuracies[0] if accuracies else None,
                "final": accuracies[-1] if accuracies else None,
                "max": max(accuracies) if accuracies else None,
                "average": sum(accuracies) / len(accuracies) if accuracies else None
            } if accuracies else None,
            "start_time": metadata.get("start_time").isoformat() if metadata.get("start_time") else None,
            "end_time": metadata.get("end_time").isoformat() if metadata.get("end_time") else None
        }

    def cleanup_old_jobs(self, max_age_hours: int = 24):
        """Clean up progress data for old completed jobs"""

        now = datetime.now()
        jobs_to_remove = []

        for job_id, metadata in self.job_metadata.items():
            if metadata.get("status") in ["completed", "failed"]:
                end_time = metadata.get("end_time")
                if end_time and (now - end_time).total_seconds() / 3600 > max_age_hours:
                    jobs_to_remove.append(job_id)

        for job_id in jobs_to_remove:
            del self.job_metadata[job_id]
            del self.progress_history[job_id]
            if job_id in self.current_progress:
                del self.current_progress[job_id]
            if job_id in self.listeners:
                del self.listeners[job_id]

        if jobs_to_remove:
            print(f"🗑️ Cleaned up {len(jobs_to_remove)} old jobs")


# Global tracker instance
_tracker_instance = None


def get_progress_tracker() -> TrainingProgressTracker:
    """Get global progress tracker instance"""
    global _tracker_instance
    if _tracker_instance is None:
        _tracker_instance = TrainingProgressTracker()
    return _tracker_instance


if __name__ == "__main__":
    # Test progress tracker
    tracker = TrainingProgressTracker()

    # Start tracking a job
    tracker.start_tracking(
        job_id=1,
        total_epochs=10,
        total_steps=100,
        training_type="lora"
    )

    # Simulate training progress
    for epoch in range(10):
        for step in range(100):
            loss = 2.5 - (epoch * 0.2) - (step * 0.001)
            accuracy = 0.5 + (epoch * 0.04) + (step * 0.0004)

            tracker.update_progress(
                job_id=1,
                epoch=epoch,
                step=step,
                loss=max(0.1, loss),
                accuracy=min(0.99, accuracy),
                learning_rate=0.0002,
                gpu_memory_mb=4096,
                samples_per_second=15.5
            )

            time.sleep(0.01)

    # Mark as completed
    tracker.mark_completed(1, success=True)

    # Get summary
    summary = tracker.get_summary_statistics(1)
    print("\n📊 Training Summary:")
    print(json.dumps(summary, indent=2))

    # Export progress
    tracker.export_progress(1, "training_progress.json")
